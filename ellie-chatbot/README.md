# Ellie Chatbot

고정 스크립트 연구용 Streamlit 챗봇입니다. Connection / Breathing 앱이 분리되어 있으며, 스크립트는 한국어입니다.

```text
ellie-chatbot/
├── connection_app.py
├── breathing_app.py
├── scripts.py
├── drive_upload.py
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
python -m streamlit run connection_app.py
python -m streamlit run breathing_app.py --server.port 8502
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

### Google Drive 준비

1. Google Cloud에서 프로젝트 생성
2. Google Drive API 사용 설정
3. 서비스 계정 생성 후 JSON 키 다운로드
4. Drive에 결과 저장용 폴더 생성
5. 폴더를 서비스 계정 이메일과 **편집자**로 공유
6. 폴더 URL의 `folders/` 뒤 문자열을 `GDRIVE_FOLDER_ID`로 설정
7. 서비스 계정 JSON 내용을 `[gcp_service_account]`에 그대로 옮김 (`private_key` 줄바꿈은 `\n`)

## Streamlit Community Cloud

같은 저장소를 앱 두 개로 배포합니다.

| 앱 | Main file path |
|----|----------------|
| Connection | `ellie-chatbot/connection_app.py` |
| Breathing | `ellie-chatbot/breathing_app.py` |

각 앱 Secrets에 OpenAI + Google Drive 값을 동일하게 넣습니다.
