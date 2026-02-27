"""
Mock Cloud Code client for Tiangan MCP.

This simulates Unity Cloud Code behavior so the MCP server can run
end‑to‑end even when Cloud Code REST is unavailable or IAM is broken.

It mirrors the real Cloud Code REST response shapes and error patterns.
"""

import random
import asyncio


class MockCloudCodeClient:
    """
    A lightweight, predictable mock of Unity Cloud Code.

    - Scripts are stored in a dictionary
    - Each script is an async function receiving `params`
    - Responses mimic Unity Cloud Code REST JSON structure
    """

    def __init__(self):
        # Register mock scripts here
        self.scripts = {
            "test_script": self._run_test_script,
            "echo": self._run_echo_script,
        }

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    async def run_script(self, script_name: str, params: dict):
        """
        Simulate running a Cloud Code script.

        Returns a dict shaped like Unity Cloud Code REST responses.
        """

        # Script not found
        if script_name not in self.scripts:
            return {
                "status": 404,
                "title": "Not Found",
                "detail": f"Script '{script_name}' does not exist in mock environment",
                "code": 54,
            }

        try:
            # Execute the script
            result = await self.scripts[script_name](params)

            # Wrap in Cloud Code response shape
            return {
                "status": 200,
                "result": result,
            }

        except Exception as e:
            # Simulate Cloud Code internal error
            return {
                "status": 500,
                "title": "Internal Error",
                "detail": str(e),
                "code": 500,
            }

    # ---------------------------------------------------------
    # Mock script implementations
    # ---------------------------------------------------------

    async def _run_test_script(self, params):
        """
        Simulates the dice‑rolling example script.
        """
        await asyncio.sleep(0.05)  # simulate network latency

        return {
            "sides": 6,
            "roll": random.randint(1, 6),
            "echo": params,
        }

    async def _run_echo_script(self, params):
        """
        A simple echo script for debugging.
        """
        await asyncio.sleep(0.01)
        return {
            "message": "Echo from mock Cloud Code",
            "params": params,
        }
