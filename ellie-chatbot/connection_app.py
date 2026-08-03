import csv
import io
import json
import time
from datetime import datetime, timezone
from typing import Any

import streamlit as st
from openai import OpenAI

from drive_upload import (
    drive_configured,
    upload_session_artifacts,
)
from scripts import SCRIPTS


APP_CONDITION = "Connection"


st.set_page_config(
    page_title="Ellie Scripted Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)


CLASSIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "answer_type": {
            "type": "string",
            "enum": ["yes", "no", "unclear", "other"],
        },
        "has_elaboration": {
            "type": "boolean",
        },
        "valid_if_then": {
            "type": "boolean",
        },
    },
    "required": [
        "answer_type",
        "has_elaboration",
        "valid_if_then",
    ],
    "additionalProperties": False,
}


CLASSIFIER_INSTRUCTIONS = """
Classify one participant response for a fixed-script research chatbot.

Do not answer the participant.
Do not generate the next study sentence.
Do not rewrite the study script.
Call the classify_participant_response function exactly once.

Rules:

answer_type
- yes: affirmative, agreement, willingness, confirmation, or a positive answer.
- no: denial, disagreement, unwillingness, no experience, no attempt,
  or no perceived benefit.
- unclear: too ambiguous to determine yes or no.
- other: yes/no is not relevant.

has_elaboration
- true: includes a concrete reason, feeling, example, personal benefit,
  situation, explanation, or intended action beyond a bare yes/no.
- false: only a short answer such as yes, no, sure, okay, or an equivalent.

valid_if_then
- true only when the participant gives an IF condition or situation,
  followed by a THEN action or plan.
- false otherwise.

The response may be in English, Korean, or another language.
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_openai_settings() -> tuple[str, str]:
    try:
        api_key = str(
            st.secrets["OPENAI_API_KEY"]
        ).strip()

        model = str(
            st.secrets.get(
                "OPENAI_MODEL",
                "gpt-5-mini",
            )
        ).strip()

    except Exception:
        api_key = ""
        model = "gpt-5-mini"

    return api_key, model


@st.cache_resource(show_spinner=False)
def create_openai_client(
    api_key: str,
) -> OpenAI:
    return OpenAI(api_key=api_key)


def parse_function_call(
    response: Any,
) -> dict[str, Any]:
    """
    Read arguments from the forced function call.

    This does not rely on response.output_text, so a response containing
    a tool call is not incorrectly treated as an empty text response.
    """
    for item in response.output:
        item_type = getattr(
            item,
            "type",
            None,
        )
        item_name = getattr(
            item,
            "name",
            None,
        )

        if (
            item_type == "function_call"
            and item_name
            == "classify_participant_response"
        ):
            arguments = getattr(
                item,
                "arguments",
                None,
            )

            if not arguments:
                raise RuntimeError(
                    "OpenAI 함수 호출에 arguments가 없습니다."
                )

            parsed = json.loads(arguments)

            return {
                "answer_type": parsed["answer_type"],
                "has_elaboration": bool(
                    parsed["has_elaboration"]
                ),
                "valid_if_then": bool(
                    parsed["valid_if_then"]
                ),
            }

    status = getattr(
        response,
        "status",
        "unknown",
    )
    incomplete_details = getattr(
        response,
        "incomplete_details",
        None,
    )

    raise RuntimeError(
        "OpenAI 함수 호출 결과가 없습니다. "
        f"status={status}, "
        f"incomplete_details={incomplete_details}"
    )


def analyze_participant_response(
    *,
    condition: str,
    step_id: int,
    prompt: str,
    participant_response: str,
) -> dict[str, Any]:
    """
    Use OpenAI only when a scripted branch or validation requires it.

    A forced function call is used instead of response.output_text.
    """
    api_key, model = load_openai_settings()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 설정되지 않았습니다."
        )

    client = create_openai_client(api_key)

    payload = {
        "condition": condition,
        "step_id": step_id,
        "script_prompt": prompt,
        "participant_response": participant_response,
    }

    last_error: Exception | None = None

    # Retry once in case the first API response is incomplete.
    for max_tokens in (800, 1600):
        try:
            response = client.responses.create(
                model=model,
                instructions=CLASSIFIER_INSTRUCTIONS,
                input=json.dumps(
                    payload,
                    ensure_ascii=False,
                ),
                tools=[
                    {
                        "type": "function",
                        "name": (
                            "classify_participant_response"
                        ),
                        "description": (
                            "Return the classification of the "
                            "participant response."
                        ),
                        "parameters": CLASSIFICATION_SCHEMA,
                        "strict": True,
                    }
                ],
                tool_choice={
                    "type": "function",
                    "name": (
                        "classify_participant_response"
                    ),
                },
                parallel_tool_calls=False,
                max_output_tokens=max_tokens,
                store=False,
            )

            result = parse_function_call(response)

            return {
                **result,
                "model": model,
                "response_id": getattr(
                    response,
                    "id",
                    None,
                ),
            }

        except Exception as error:
            last_error = error

    raise RuntimeError(
        "OpenAI 응답 분석에 실패했습니다. "
        f"{type(last_error).__name__}: {last_error}"
    )


def add_message(
    role: str,
    content: str,
    step_id: int | None,
    kind: str,
) -> None:
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "step_id": step_id,
            "kind": kind,
            "timestamp_utc": utc_now_iso(),
        }
    )


def current_script() -> list[dict[str, Any]]:
    return SCRIPTS[
        st.session_state.condition
    ]


def get_step(
    step_id: int,
) -> dict[str, Any]:
    for step in current_script():
        if step["id"] == step_id:
            return step

    raise KeyError(
        f"Unknown step id: {step_id}"
    )


def set_waiting_context(
    *,
    kind: str,
    step_id: int,
    prompt: str,
) -> None:
    st.session_state.waiting_context = {
        "kind": kind,
        "step_id": step_id,
        "prompt": prompt,
    }
    st.session_state.prompt_started_monotonic = (
        time.monotonic()
    )


def show_numbered_step(
    step: dict[str, Any],
) -> None:
    """
    Show exactly one numbered script line and always wait for a response.

    The original expects_input value is intentionally ignored because every
    numbered item must wait for participant input.
    """
    add_message(
        role="assistant",
        content=step["text"],
        step_id=step["id"],
        kind="script",
    )

    st.session_state.current_step_id = (
        step["id"]
    )

    set_waiting_context(
        kind="numbered",
        step_id=step["id"],
        prompt=step["text"],
    )


def show_next_numbered_step() -> None:
    script = current_script()
    index = st.session_state.next_step_index

    if index >= len(script):
        finish_session()
        return

    step = script[index]
    st.session_state.next_step_index += 1

    show_numbered_step(step)


def show_auxiliary_prompt(
    *,
    content: str,
    step_id: int,
    waiting_kind: str,
    message_kind: str,
) -> None:
    """
    Show one conditional or correction line and wait for a response.

    It also obeys the one-assistant-turn / one-human-turn rule.
    """
    add_message(
        role="assistant",
        content=content,
        step_id=step_id,
        kind=message_kind,
    )

    set_waiting_context(
        kind=waiting_kind,
        step_id=step_id,
        prompt=content,
    )


def initialize_session(
    participant_id: str,
    condition: str,
) -> None:
    st.session_state.started = True
    st.session_state.finished = False

    st.session_state.participant_id = (
        participant_id.strip()
    )
    st.session_state.condition = condition

    st.session_state.next_step_index = 0
    st.session_state.current_step_id = None
    st.session_state.waiting_context = None

    st.session_state.messages = []
    st.session_state.responses = []
    st.session_state.api_analyses = []
    st.session_state.last_api_error = None
    st.session_state.drive_upload_status = None
    st.session_state.drive_file_ids = None

    st.session_state.started_at_utc = (
        utc_now_iso()
    )
    st.session_state.finished_at_utc = None
    st.session_state.elapsed_seconds = None

    st.session_state.session_started_monotonic = (
        time.monotonic()
    )
    st.session_state.prompt_started_monotonic = None

    # Start with number 1 only.
    show_next_numbered_step()


def finish_session() -> None:
    if st.session_state.finished:
        return

    st.session_state.finished = True
    st.session_state.waiting_context = None
    st.session_state.finished_at_utc = (
        utc_now_iso()
    )
    st.session_state.elapsed_seconds = round(
        time.monotonic()
        - st.session_state.session_started_monotonic,
        3,
    )
    upload_results_to_drive()


def upload_results_to_drive() -> None:
    if st.session_state.drive_upload_status == "success":
        return

    if not drive_configured():
        st.session_state.drive_upload_status = (
            "skipped_not_configured"
        )
        return

    base_name = (
        f"{st.session_state.participant_id}_"
        f"{st.session_state.condition.lower()}_"
        f"{st.session_state.finished_at_utc.replace(':', '-')}"
    )

    try:
        file_ids = upload_session_artifacts(
            base_name=base_name,
            json_bytes=result_json_bytes(),
            csv_bytes=result_csv_bytes(),
        )
        st.session_state.drive_file_ids = file_ids
        st.session_state.drive_upload_status = "success"
    except Exception as error:
        st.session_state.drive_upload_status = (
            f"failed: {type(error).__name__}: {error}"
        )


def reset_session() -> None:
    for key in list(
        st.session_state.keys()
    ):
        del st.session_state[key]

    st.rerun()


def save_user_response(
    *,
    user_text: str,
    step_id: int,
    prompt: str,
    response_kind: str,
) -> None:
    started = (
        st.session_state.prompt_started_monotonic
    )

    response_time = None

    if started is not None:
        response_time = round(
            time.monotonic() - started,
            3,
        )

    st.session_state.responses.append(
        {
            "participant_id": (
                st.session_state.participant_id
            ),
            "condition": (
                st.session_state.condition
            ),
            "step_id": step_id,
            "prompt": prompt,
            "response": user_text,
            "response_kind": response_kind,
            "response_time_seconds": (
                response_time
            ),
            "timestamp_utc": utc_now_iso(),
        }
    )


def save_api_analysis(
    *,
    step_id: int,
    analysis: dict[str, Any],
) -> None:
    st.session_state.api_analyses.append(
        {
            "step_id": step_id,
            "answer_type": (
                analysis["answer_type"]
            ),
            "has_elaboration": (
                analysis["has_elaboration"]
            ),
            "valid_if_then": (
                analysis["valid_if_then"]
            ),
            "model": analysis["model"],
            "response_id": (
                analysis["response_id"]
            ),
            "timestamp_utc": utc_now_iso(),
        }
    )


def analyze_or_show_retry(
    *,
    step_id: int,
    prompt: str,
    user_text: str,
) -> dict[str, Any] | None:
    try:
        analysis = analyze_participant_response(
            condition=st.session_state.condition,
            step_id=step_id,
            prompt=prompt,
            participant_response=user_text,
        )

        save_api_analysis(
            step_id=step_id,
            analysis=analysis,
        )

        st.session_state.last_api_error = None
        return analysis

    except Exception as error:
        st.session_state.last_api_error = (
            f"{type(error).__name__}: {error}"
        )

        show_auxiliary_prompt(
            content=(
                "Sorry, I didn't catch that. "
                "Could you say that again?"
            ),
            step_id=step_id,
            waiting_kind="api_retry",
            message_kind="api_error",
        )

        return None


def process_numbered_response(
    *,
    step_id: int,
    prompt: str,
    user_text: str,
) -> None:
    step = get_step(step_id)

    # API is called only where the supplied script has a branch or validator.
    needs_api = bool(
        step.get("branch")
        or step.get("validator")
    )

    analysis: dict[str, Any] | None = None

    if needs_api:
        analysis = analyze_or_show_retry(
            step_id=step_id,
            prompt=prompt,
            user_text=user_text,
        )

        if analysis is None:
            return

    # Number 7: explicit If No branch.
    if (
        step.get("branch") == "experience"
        and analysis is not None
        and analysis["answer_type"] == "no"
    ):
        show_auxiliary_prompt(
            content=step["if_no"],
            step_id=step_id,
            waiting_kind="branch_ack",
            message_kind="conditional",
        )
        return

    # Number 11: explicit No and Yes-without-elaboration branches.
    if (
        step.get("branch") == "benefit"
        and analysis is not None
    ):
        if analysis["answer_type"] == "no":
            show_auxiliary_prompt(
                content=step["if_no"],
                step_id=step_id,
                waiting_kind="branch_ack",
                message_kind="conditional",
            )
            return

        if (
            analysis["answer_type"] == "yes"
            and not analysis["has_elaboration"]
        ):
            show_auxiliary_prompt(
                content=(
                    step[
                        "if_yes_without_elaboration"
                    ]
                ),
                step_id=step_id,
                waiting_kind=(
                    "benefit_elaboration"
                ),
                message_kind="conditional",
            )
            return

    # Number 19: explicit IF–THEN validation.
    if (
        step.get("validator") == "if_then"
        and analysis is not None
        and not analysis["valid_if_then"]
    ):
        show_auxiliary_prompt(
            content=step["invalid_response"],
            step_id=step_id,
            waiting_kind="if_then_retry",
            message_kind="validation",
        )
        return

    # One human response produces one next numbered assistant message.
    show_next_numbered_step()


def process_if_then_retry(
    *,
    step_id: int,
    prompt: str,
    user_text: str,
) -> None:
    analysis = analyze_or_show_retry(
        step_id=step_id,
        prompt=prompt,
        user_text=user_text,
    )

    if analysis is None:
        return

    step = get_step(step_id)

    if not analysis["valid_if_then"]:
        show_auxiliary_prompt(
            content=step["invalid_response"],
            step_id=step_id,
            waiting_kind="if_then_retry",
            message_kind="validation",
        )
        return

    show_next_numbered_step()


def process_api_retry(
    *,
    step_id: int,
    user_text: str,
) -> None:
    """
    Re-run the original numbered step analysis after an API failure.

    The original numbered prompt is recovered from scripts.py.
    """
    step = get_step(step_id)

    process_numbered_response(
        step_id=step_id,
        prompt=step["text"],
        user_text=user_text,
    )


def process_user_input(
    user_text: str,
) -> None:
    context = (
        st.session_state.waiting_context
    )

    if context is None:
        return

    waiting_kind = context["kind"]
    step_id = context["step_id"]
    prompt = context["prompt"]

    add_message(
        role="user",
        content=user_text,
        step_id=step_id,
        kind="response",
    )

    save_user_response(
        user_text=user_text,
        step_id=step_id,
        prompt=prompt,
        response_kind=waiting_kind,
    )

    st.session_state.waiting_context = None

    if waiting_kind == "numbered":
        process_numbered_response(
            step_id=step_id,
            prompt=prompt,
            user_text=user_text,
        )
        return

    if waiting_kind == "if_then_retry":
        process_if_then_retry(
            step_id=step_id,
            prompt=prompt,
            user_text=user_text,
        )
        return

    if waiting_kind == "api_retry":
        process_api_retry(
            step_id=step_id,
            user_text=user_text,
        )
        return

    if waiting_kind in {
        "branch_ack",
        "benefit_elaboration",
    }:
        show_next_numbered_step()
        return

    raise RuntimeError(
        f"Unknown waiting kind: {waiting_kind}"
    )


def result_payload() -> dict[str, Any]:
    return {
        "participant_id": (
            st.session_state.participant_id
        ),
        "condition": (
            st.session_state.condition
        ),
        "started_at_utc": (
            st.session_state.started_at_utc
        ),
        "finished_at_utc": (
            st.session_state.finished_at_utc
        ),
        "elapsed_seconds": (
            st.session_state.elapsed_seconds
        ),
        "responses": (
            st.session_state.responses
        ),
        "api_analyses": (
            st.session_state.api_analyses
        ),
        "messages": (
            st.session_state.messages
        ),
    }


def result_json_bytes() -> bytes:
    return json.dumps(
        result_payload(),
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")


def result_csv_bytes() -> bytes:
    output = io.StringIO()

    fieldnames = [
        "participant_id",
        "condition",
        "step_id",
        "prompt",
        "response",
        "response_kind",
        "response_time_seconds",
        "timestamp_utc",
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(
        st.session_state.responses
    )

    return output.getvalue().encode(
        "utf-8-sig"
    )


api_key, selected_model = (
    load_openai_settings()
)

if not api_key:
    st.error(
        "OpenAI API 키가 설정되지 않았습니다. "
        "`.streamlit/secrets.toml`에 "
        "`OPENAI_API_KEY`를 입력해주세요."
    )
    st.stop()


if "started" not in st.session_state:
    st.session_state.started = False


st.title("Ellie")
st.caption("Fixed-script research chatbot")


if not st.session_state.started:
    st.subheader("Session setup")

    with st.form("session_setup"):
        participant_id = st.text_input(
            "Participant ID",
            placeholder="Example: P001",
        )

        submitted = (
            st.form_submit_button(
                "Start session",
                use_container_width=True,
            )
        )

    if submitted:
        if not participant_id.strip():
            st.error(
                "Participant ID를 입력해주세요."
            )
        else:
            initialize_session(
                participant_id,
                APP_CONDITION,
            )
            st.rerun()

    st.stop()


with st.sidebar:
    st.subheader("Researcher view")

    st.write(
        "Participant: "
        f"`{st.session_state.participant_id}`"
    )
    st.write(
        "Condition: "
        f"`{APP_CONDITION}`"
    )
    st.write(
        "OpenAI model: "
        f"`{selected_model}`"
    )
    st.write(
        "Current step: "
        f"`{st.session_state.current_step_id}`"
    )
    st.write(
        "API analyses: "
        f"`{len(st.session_state.api_analyses)}`"
    )

    if st.session_state.finished:
        st.write(
            "Current state: `Finished`"
        )
    else:
        context = (
            st.session_state.waiting_context
        )

        state_text = (
            context["kind"]
            if context
            else "processing"
        )

        st.write(
            "Current state: "
            f"`{state_text}`"
        )

    if st.session_state.last_api_error:
        st.error(
            "Last API error\n\n"
            f"`{st.session_state.last_api_error}`"
        )

    drive_status = st.session_state.get(
        "drive_upload_status"
    )
    if drive_status:
        st.write(
            "Drive upload: "
            f"`{drive_status}`"
        )

    if st.button(
        "Restart session",
        use_container_width=True,
    ):
        reset_session()


for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


if not st.session_state.finished:
    user_text = st.chat_input(
        "Type your answer"
    )

    if user_text:
        with st.spinner(
            "Processing..."
        ):
            process_user_input(
                user_text
            )

        st.rerun()


if st.session_state.finished:
    st.success(
        "The session is complete. "
        "Thank you for your participation."
    )
