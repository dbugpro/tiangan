import os
import requests

UNITY_CLIENT_ID = os.getenv("UNITY_CLIENT_ID")
UNITY_CLIENT_SECRET = os.getenv("UNITY_CLIENT_SECRET")
UNITY_ORG_ID = os.getenv("UNITY_ORG_ID")
UNITY_SCOPE = os.getenv("UNITY_SCOPE", "cloud-platform")
UNITY_AUDIENCE = os.getenv("UNITY_AUDIENCE", "unity")


# ============================================================
# UNITY CLOUD AUTH
# ============================================================

def get_unity_access_token():
    token_url = "https://services.api.unity.com/auth/v1/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": UNITY_CLIENT_ID,
        "client_secret": UNITY_CLIENT_SECRET,
        "scope": UNITY_SCOPE,
        "audience": UNITY_AUDIENCE,
    }

    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        raise Exception(f"Unity OAuth failed: {response.text}")

    return response.json()["access_token"]


# ============================================================
# TOOL: list_unity_projects
# ============================================================

def list_unity_projects():
    token = get_unity_access_token()

    url = f"https://services.api.unity.com/projects/v1/projects?orgId={UNITY_ORG_ID}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Unity Projects API failed: {response.text}")

    return response.json()


# ============================================================
# TOOL: list_unity_environments
# ============================================================

def list_unity_environments(project_id: str):
    token = get_unity_access_token()

    url = f"https://services.api.unity.com/environments/v1/projects/{project_id}/environments"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Unity Environments API failed: {response.text}")

    return response.json()
