# Ellie Chatbot

고정 스크립트 연구용 Streamlit 챗봇입니다. 조건별 앱이 분리되어 있으며, 스크립트는 한국어입니다.

## 조건 / 앱 파일

| 조건 | Main file path | 추천 URL |
|------|----------------|----------|
| Humor + Social Connection | `ellie-chatbot/humor_social_app.py` | `ellie-humor-social.streamlit.app` |
| Social Connection | `ellie-chatbot/social_connection_app.py` | `ellie-social-connection.streamlit.app` |
| Control | `ellie-chatbot/control_app.py` | `ellie-control.streamlit.app` |

```text
ellie-chatbot/
├── humor_social_app.py
├── social_connection_app.py
├── control_app.py
├── chatbot_core.py
├── scripts.py
├── drive_upload.py
├── ui_helpers.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## 로컬 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
```

```powershell
python -m streamlit run humor_social_app.py
python -m streamlit run social_connection_app.py --server.port 8502
python -m streamlit run control_app.py --server.port 8503
```

## Secrets

`.streamlit/secrets.toml` (로컬) 또는 Streamlit Community Cloud Secrets:

```toml
OPENAI_API_KEY = "실제_API_KEY"
OPENAI_MODEL = "gpt-5-mini"
GDRIVE_FOLDER_ID = "구글드라이브_폴더_ID"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

세션이 끝나면 참가자에게 다운로드 버튼은 보이지 않고, JSON/CSV가 Google Drive 폴더로 자동 업로드됩니다.

## Streamlit Community Cloud

같은 저장소를 앱 세 개로 배포합니다. 각 앱 Secrets에 OpenAI + Google Drive 값을 동일하게 넣습니다.

기존 Connection / Breathing 앱이 있다면 새 Main file path로 바꾸거나 앱을 새로 만든 뒤 이전 앱은 삭제하면 됩니다.
