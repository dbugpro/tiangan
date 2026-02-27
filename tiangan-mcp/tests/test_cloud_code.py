import asyncio
from tools.mock_cloud_code import MockCloudCodeClient

async def main():
    client = MockCloudCodeClient()
    result = await client.run_script("test_script", {"foo": "bar"})
    print("Mock Cloud Code result:", result)

asyncio.run(main())
