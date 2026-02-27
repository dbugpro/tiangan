"""
UGS REST client for Tiangan MCP.

This client handles:
  - Base64 Project API Key authentication
  - JSON POST requests
  - Cloud Save (set/get)
  - Easy extension for other UGS services

It is intentionally minimal and predictable.
"""

import base64
import aiohttp


class UGSRestClient:
    """
    A lightweight async REST client for Unity Gaming Services.

    Supports:
      - Cloud Save (set/get)
      - Generic POST helper
    """

    def __init__(self, project_id: str, environment_id: str, api_key: str):
        self.project_id = project_id
        self.environment_id = environment_id
        self.api_key = api_key

        # Unity Cloud uses Basic Auth with API key as username and empty password
        token = base64.b64encode(f"{api_key}:".encode()).decode()

        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    # ---------------------------------------------------------
    # Internal HTTP helper
    # ---------------------------------------------------------

    async def _post(self, url: str, payload: dict):
        """
        Generic POST helper with JSON body and Basic Auth.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as resp:
                try:
                    return await resp.json()
                except Exception:
                    # Fallback if Unity returns non‑JSON error
                    return {
                        "status": resp.status,
                        "error": "Non‑JSON response from Unity Cloud",
                        "text": await resp.text(),
                    }

    # ---------------------------------------------------------
    # Cloud Save
    # ---------------------------------------------------------

    async def cloud_save_set(self, key: str, value):
        """
        Set a Cloud Save key/value pair.

        Equivalent to:
          POST /cloud-save/v1/data/projects/{projectId}/environments/{environmentId}/items
        """
        url = (
            f"https://services.api.unity.com/cloud-save/v1/data/projects/"
            f"{self.project_id}/environments/{self.environment_id}/items"
        )

        payload = {
            "data": [
                {
                    "key": key,
                    "value": value,
                }
            ]
        }

        return await self._post(url, payload)

    async def cloud_save_get(self, key: str):
        """
        Get a Cloud Save key.

        Equivalent to:
          POST /cloud-save/v1/data/projects/{projectId}/environments/{environmentId}/items/{key}
        """
        url = (
            f"https://services.api.unity.com/cloud-save/v1/data/projects/"
            f"{self.project_id}/environments/{self.environment_id}/items/{key}"
        )

        # Cloud Save GET is actually a POST with empty body
        return await self._post(url, {})
