"""Upload session result files to Google Drive via a service account."""

from __future__ import annotations

import io
from typing import Any

import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


DRIVE_SCOPE = ("https://www.googleapis.com/auth/drive.file",)


def drive_configured() -> bool:
    try:
        folder_id = str(
            st.secrets.get("GDRIVE_FOLDER_ID", "")
        ).strip()
        account = st.secrets.get(
            "gcp_service_account"
        )
        return bool(folder_id and account)
    except Exception:
        return False


def _drive_service():
    info = dict(st.secrets["gcp_service_account"])
    credentials = (
        service_account.Credentials.from_service_account_info(
            info,
            scopes=DRIVE_SCOPE,
        )
    )
    return build(
        "drive",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


def _upload_bytes(
    *,
    service: Any,
    folder_id: str,
    filename: str,
    data: bytes,
    mime_type: str,
) -> str:
    metadata = {
        "name": filename,
        "parents": [folder_id],
    }
    media = MediaIoBaseUpload(
        io.BytesIO(data),
        mimetype=mime_type,
        resumable=False,
    )
    created = (
        service.files()
        .create(
            body=metadata,
            media_body=media,
            fields="id,name",
            supportsAllDrives=True,
        )
        .execute()
    )
    return str(created["id"])


def upload_session_artifacts(
    *,
    base_name: str,
    json_bytes: bytes,
    csv_bytes: bytes,
) -> dict[str, str]:
    """
    Upload JSON and CSV result files to the configured Drive folder.

    Returns a dict with uploaded file ids.
    """
    if not drive_configured():
        raise RuntimeError(
            "Google Drive secrets are not configured. "
            "Set GDRIVE_FOLDER_ID and [gcp_service_account]."
        )

    folder_id = str(
        st.secrets["GDRIVE_FOLDER_ID"]
    ).strip()
    service = _drive_service()

    json_id = _upload_bytes(
        service=service,
        folder_id=folder_id,
        filename=f"{base_name}.json",
        data=json_bytes,
        mime_type="application/json",
    )
    csv_id = _upload_bytes(
        service=service,
        folder_id=folder_id,
        filename=f"{base_name}.csv",
        data=csv_bytes,
        mime_type="text/csv",
    )

    return {
        "json_file_id": json_id,
        "csv_file_id": csv_id,
    }
