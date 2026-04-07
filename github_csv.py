import base64
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

REPO = "mikelfc12/L5s"
BRANCH = "main"


def load_csv(file_path, columns):
    token = st.secrets.get("GITHUB_TOKEN")
    if token:
        return _load_csv_from_github(file_path, columns, token)

    local_path = Path(file_path)
    if not local_path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(local_path)


def save_csv(file_path, df, commit_message):
    token = st.secrets.get("GITHUB_TOKEN")
    if token:
        _save_csv_to_github(file_path, df, commit_message, token)
        return

    df.to_csv(file_path, index=False)


def _load_csv_from_github(file_path, columns, token):
    response = requests.get(_github_url(file_path), headers=_headers(token), timeout=30)

    if response.status_code == 404:
        return pd.DataFrame(columns=columns)

    response.raise_for_status()
    payload = response.json()
    content = base64.b64decode(payload["content"]).decode("utf-8")
    if not content.strip():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(StringIO(content))


def _save_csv_to_github(file_path, df, commit_message, token):
    get_response = requests.get(_github_url(file_path), headers=_headers(token), timeout=30)
    sha = None

    if get_response.status_code == 200:
        sha = get_response.json()["sha"]
    elif get_response.status_code != 404:
        get_response.raise_for_status()

    encoded_content = base64.b64encode(df.to_csv(index=False).encode()).decode()
    data = {
        "message": commit_message,
        "content": encoded_content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha

    put_response = requests.put(_github_url(file_path), headers=_headers(token), json=data, timeout=30)
    put_response.raise_for_status()


def _github_url(file_path):
    return f"https://api.github.com/repos/{REPO}/contents/{file_path}"


def _headers(token):
    return {"Authorization": f"token {token}"}
