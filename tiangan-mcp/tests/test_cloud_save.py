import asyncio
from tools.ugs_rest_client import UGSRestClient

async def main():
    client = UGSRestClient(
        project_id="ccab5e18-e5b5-4702-8de8-1f97eed80ba1",
        environment_id="936fe4cd-9d75-4ac6-9130-bb2149c1481a",
        api_key="9c74453d0c48a658dba04b30d9a38e64"
    )

    print(await client.cloud_save_set("testKey", {"hello": "world"}))
    print(await client.cloud_save_get("testKey"))

asyncio.run(main())
