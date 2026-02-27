import base64
import json
import aiohttp

class UGSRestClient:
    def __init__(self, project_id, environment_id, api_key):
        self.project_id = project_id
        self.environment_id = environment_id
        self.api_key = api_key

        token = base64.b64encode(f"{api_key}:".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    async def post(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as resp:
                return await resp.json()

    async def cloud_save_set(self, key, value):
        url = f"https://services.api.unity.com/cloud-save/v1/data/projects/{self.project_id}/environments/{self.environment_id}/items"
        payload = {
            "data": [
                {
                    "key": key,
                    "value": value
                }
            ]
        }
        return await self.post(url, payload)

    async def cloud_save_get(self, key):
        url = f"https://services.api.unity.com/cloud-save/v1/data/projects/{self.project_id}/environments/{self.environment_id}/items/{key}"
        return await self.post(url, {})
