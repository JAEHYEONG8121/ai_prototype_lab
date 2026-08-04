"""Fixed Korean scripts transcribed from ellie_scripts.docx.

The chatbot must not generate or rewrite these prompts. The application only
selects the correct condition, advances through the numbered steps, and applies
the explicit conditional responses included in the source document.

Branch / validator metadata is preserved so existing OpenAI classification
logic continues to work unchanged.
"""

CONNECTION_STEPS = [
    {
        "id": 1,
        "text": (
            "안녕하세요, 저는 엘리라고 해요. 만나서 반갑습니다! "
            "방금 글을 읽고 느낀 점을 편하게 말씀해 주세요."
        ),
        "expects_input": True,
    },
    {
        "id": 2,
        "text": (
            "얘기해 주셔서 감사합니다! 방금 읽으신 글은 친하지 않은 사람들과 "
            "순간순간 느끼는 연결감을 굉장히 강조했죠. 이 얘기가 얼마나 와닿으셨나요?"
        ),
        "expects_input": True,
    },
    {
        "id": 3,
        "text": "이렇게 잘 알지 못하는 상대와 연결감을 느끼신 적이 있나요?",
        "expects_input": True,
        "branch": "experience",
        "if_no": "그렇다면 그런 경험을 했을 때 어떨지 상상해 보세요.",
    },
    {
        "id": 4,
        "text": (
            "어떤 느낌인지 조금 설명해 주실 수 있나요? "
            "저는 그럴 일이 없으니, 어떤 기분일지 궁금하네요."
        ),
        "expects_input": True,
    },
    {
        "id": 5,
        "text": (
            "이 연구의 목적은 사람들이 행동 목표를 세우고 실행으로 옮기면 "
            "어떤 일이 벌어질지 알아보는 것이에요. 행동 목표를 세우고 "
            "실천하려고 노력할 의향이 있으신가요?"
        ),
        "expects_input": True,
    },
    {
        "id": 6,
        "text": (
            "읽으신 글은 이 행동을 실천하는 것의 다양한 이점들을 언급하죠. "
            "이 외에도 더 많은 이점들이 있을 수 있고요! 이 행동을 통해 얻을 수 "
            "있는 이점 중, 본인의 가치관에 잘 맞는 이점은 무엇이 있을까요?"
        ),
        "expects_input": True,
        "branch": "benefit",
        "if_no": (
            "장점이 없을 것 같다니, 대단히 아쉽군요. 연구진은 친하지 않은 "
            "사람들과 연결감을 경험하는 것이 중요하다고 하니, 저는 일단 "
            "대화를 이어갈게요."
        ),
        "if_yes_without_elaboration": (
            "좋습니다! 더 자세히 알려주실 수 있나요? "
            "개인적으로 어떤 이점이 있을 것 같나요?"
        ),
    },
    {
        "id": 7,
        "text": (
            "이제, 다음 24시간 동안 친하지 않은 사람들과 연결감을 느끼려고 "
            "최선을 다해 노력해보세요. 사람들과 눈도 더 마주치고, 웃어줄 수도 "
            "있고요. 사람들의 말에도 더 귀 기울여 들어주고, 정말 서로 함께 "
            "긍정적인 감정을 공유하려고 노력해보세요."
        ),
        "expects_input": False,
    },
    {
        "id": 8,
        "text": "다음 24시간 동안 어떤 일들이 벌어질지 상상해보세요.",
        "expects_input": True,
    },
    {
        "id": 9,
        "text": "이 시간 동안 사람들과 연결감을 느낄 수 있는 기회가 있나요?",
        "expects_input": True,
    },
    {
        "id": 10,
        "text": "이러한 기회에 대해 더 생생히 떠올린 후 자세히 설명해주세요.",
        "expects_input": True,
    },
    {
        "id": 11,
        "text": (
            "연구에 따르면 “만약 ~다면, ~것이다”의 형식으로 계획을 세우는 것은, "
            "적절한 때에 적절한 방식으로 의도된 행동을 실천하도록 돕는다고 합니다. "
            "예시를 들어볼게요: “만약 모르는 사람이 내 옆에 앉는다면, 나는 나 "
            "자신을 소개하고 스몰토크를 시도할 것이다.”"
        ),
        "expects_input": False,
    },
    {
        "id": 12,
        "text": "이제, 이 형태로 스스로 실천할 목표를 2개 세워보세요.",
        "expects_input": True,
        "validator": "if_then",
        "invalid_response": (
            "올바른 형식으로 입력해 주세요! "
            "(만약 [특정 상황에 마주한]다면, [나는 이렇게 행동할] 것이다)"
        ),
    },
    {
        "id": 13,
        "text": (
            "잘 하셨습니다! 이제, 이런 기회가 찾아왔을 때 친하지 않은 사람들과 "
            "연결되는 것을 실천하지 못하게 할만한 요소는 무엇이 있을 수 있을까요?"
        ),
        "expects_input": True,
    },
    {
        "id": 14,
        "text": "어떻게 하면 이것을 극복할 수 있을까요?",
        "expects_input": True,
    },
    {
        "id": 15,
        "text": (
            "이제, “만약 ~다면, ~것이다”의 형식을 사용해서 작성해보세요. "
            "말씀하신 방해 요소와 이것을 어떻게 극복할 수 있는지 작성해주세요."
        ),
        "expects_input": True,
    },
    {
        "id": 16,
        "text": (
            "잘하셨어요! 이제 저와의 대화는 끝났습니다. 기존의 설문으로 "
            "돌아가셔서 코드 <67>을 입력 후 실험을 마무리해 주세요. "
            "사람들과 연결감을 찾으며 행복한 하루 보내시기 바랄게요, 안녕!"
        ),
        "expects_input": False,
    },
]


BREATHING_STEPS = [
    {
        "id": 1,
        "text": (
            "안녕하세요, 저는 엘리라고 해요. 만나서 반갑습니다! "
            "방금 글을 읽고 느낀 점을 편하게 말씀해 주세요."
        ),
        "expects_input": True,
    },
    {
        "id": 2,
        "text": (
            "얘기해 주셔서 감사합니다! 방금 읽으신 글은 올바른 호흡법을 "
            "굉장히 강조했죠. 이 얘기가 얼마나 와닿으셨나요?"
        ),
        "expects_input": True,
    },
    {
        "id": 3,
        "text": "이렇게 목과 어깨를 이완하고 배로 숨을 쉬어본 적이 있나요?",
        "expects_input": True,
        "branch": "experience",
        "if_no": "그렇다면 지금 한번 시도해보세요.",
    },
    {
        "id": 4,
        "text": (
            "어떤 느낌인지 조금 설명해 주실 수 있나요? "
            "저는 해볼 수 없으니, 어떤 기분일지 궁금하네요."
        ),
        "expects_input": True,
    },
    {
        "id": 5,
        "text": (
            "이 연구의 목적은 사람들이 행동 목표를 세우고 실행으로 옮기면 "
            "어떤 일이 벌어질지 알아보는 것이에요. 행동 목표를 세우고 "
            "실천하려고 노력할 의향이 있으신가요?"
        ),
        "expects_input": True,
    },
    {
        "id": 6,
        "text": (
            "읽으신 글은 이 행동을 실천하는 것의 다양한 이점들을 언급하죠. "
            "이 외에도 더 많은 이점들이 있을 수 있고요! 이 행동을 통해 얻을 수 "
            "있는 이점 중, 본인의 가치관에 잘 맞는 이점은 무엇이 있을까요?"
        ),
        "expects_input": True,
        "branch": "benefit",
        "if_no": (
            "장점이 없을 것 같다니, 대단히 아쉽군요. 연구진은 배로 호흡을 "
            "하는 것이 중요하다고 하니, 저는 일단 대화를 이어갈게요."
        ),
        "if_yes_without_elaboration": (
            "좋습니다! 더 자세히 알려주실 수 있나요? "
            "개인적으로 어떤 이점이 있을 것 같나요?"
        ),
    },
    {
        "id": 7,
        "text": (
            "이제, 다음 24시간 동안 배로 호흡을 하려고 최선을 다해 노력해보세요. "
            "어깨를 가만히 두고, 갈비뼈가 팽창하는지도 느껴볼 수 있고요. "
            "정말 배로만 깊게 숨을 쉬려고 노력해보세요."
        ),
        "expects_input": False,
    },
    {
        "id": 8,
        "text": "다음 24시간 동안 어떤 일들이 벌어질지 상상해보세요.",
        "expects_input": True,
    },
    {
        "id": 9,
        "text": "이 시간 동안 올바른 호흡법을 연습할 기회가 있나요?",
        "expects_input": True,
    },
    {
        "id": 10,
        "text": "이러한 기회에 대해 더 생생히 떠올린 후 자세히 설명해주세요.",
        "expects_input": True,
    },
    {
        "id": 11,
        "text": (
            "연구에 따르면 “만약 ~다면, ~것이다”의 형식으로 계획을 세우는 것은, "
            "적절한 때에 적절한 방식으로 의도된 행동을 실천하도록 돕는다고 합니다. "
            "예시를 들어볼게요: “만약 나에게 쉬는 시간이 생긴다면, 나는 어깨를 "
            "이완시키고 복부와 등이 팽창하도록 깊은 호흡을 시도할 것이다.”"
        ),
        "expects_input": False,
    },
    {
        "id": 12,
        "text": "이제, 이 형태로 스스로 실천할 목표를 2개 세워보세요.",
        "expects_input": True,
        "validator": "if_then",
        "invalid_response": (
            "올바른 형식으로 입력해 주세요! "
            "(만약 [특정 상황에 마주한]다면, [나는 이렇게 행동할] 것이다)"
        ),
    },
    {
        "id": 13,
        "text": (
            "잘 하셨습니다! 이제, 이런 기회가 찾아왔을 때 배로 숨을 쉬는 것을 "
            "실천하지 못하게 할만한 요소는 무엇이 있을 수 있을까요?"
        ),
        "expects_input": True,
    },
    {
        "id": 14,
        "text": "어떻게 하면 이것을 극복할 수 있을까요?",
        "expects_input": True,
    },
    {
        "id": 15,
        "text": (
            "이제, “만약 ~다면, ~것이다”의 형식을 사용해서 작성해보세요. "
            "말씀하신 방해 요소와 이것을 어떻게 극복할 수 있는지 작성해주세요."
        ),
        "expects_input": True,
    },
    {
        "id": 16,
        "text": (
            "잘하셨어요! 이제 저와의 대화는 끝났습니다. 기존의 설문으로 "
            "돌아가셔서 코드 <67>을 입력 후 실험을 마무리해 주세요. "
            "복식호흡을 연습하며 행복한 하루 보내시기 바랄게요, 안녕!"
        ),
        "expects_input": False,
    },
]


SCRIPTS = {
    "Connection": CONNECTION_STEPS,
    "Breathing": BREATHING_STEPS,
}
