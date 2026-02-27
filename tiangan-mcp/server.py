import os
import base64
import asyncio
from dataclasses import dataclass

from fastmcp import MCP, Tool, Context

from tools.mock_cloud_code import MockCloudCodeClient
from tools.ugs_rest_client import UGSRestClient


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

@dataclass
class ServerConfig:
    mode: str
    project_id: str
    environment_id: str
    api_key: str

    @classmethod
    def from_env(cls):
        mode = os.getenv("MCP_MODE", "mock").lower()

        project_id = os.getenv("UNITY_PROJECT_ID", "").strip()
        environment_id = os.getenv("UNITY_ENVIRONMENT_ID", "").strip()
        api_key = os.getenv("UNITY_API_KEY", "").strip()

        if mode not in ("mock", "rest"):
            raise ValueError("MCP_MODE must be 'mock' or 'rest'")

        if mode == "rest":
            missing = []
            if not project_id:
                missing.append("UNITY_PROJECT_ID")
            if not environment_id:
                missing.append("UNITY_ENVIRONMENT_ID")
            if not api_key:
                missing.append("UNITY_API_KEY")
            if missing:
                raise ValueError(
                    f"MCP_MODE=rest but missing required env vars: {', '.join(missing)}"
                )

        return cls(
            mode=mode,
            project_id=project_id,
            environment_id=environment_id,
            api_key=api_key,
        )


# ---------------------------------------------------------
# MCP Server
# ---------------------------------------------------------

class TianganMCP(MCP):
    """
    Your real MCP server entrypoint.

    - In mock mode: uses MockCloudCodeClient
    - In rest mode: uses UGSRestClient for Cloud Save, etc.
    """

    def __init__(self, config: ServerConfig):
        super().__init__(name="tiangan-mcp")

        self.config = config

        # Always available
        self.mock_cloud_code = MockCloudCodeClient()

        # Real UGS REST client (only in rest mode)
        self.ugs_rest = None
        if config.mode == "rest":
            self.ugs_rest = UGSRestClient(
                project_id=config.project_id,
                environment_id=config.environment_id,
                api_key=config.api_key,
            )

        # Register MCP tools
        self.register_tool(self.run_cloud_code)
        self.register_tool(self.cloud_save_set)
        self.register_tool(self.cloud_save_get)

    # -----------------------------------------------------
    # Cloud Code (mock for now)
    # -----------------------------------------------------

    @Tool
    async def run_cloud_code(self, ctx: Context, script_name: str, params: dict):
        """
        Run a Cloud Code script.

        For now:
          - Always uses mock Cloud Code
        Later:
          - Will call real Cloud Code REST once IAM is fixed
        """
        return await self.mock_cloud_code.run_script(script_name, params)

    # -----------------------------------------------------
    # Cloud Save (real REST in rest mode)
    # -----------------------------------------------------

    @Tool
    async def cloud_save_set(self, ctx: Context, key: str, value: dict):
        """
        Set a Cloud Save key/value pair.
        """
        if self.config.mode != "rest" or self.ugs_rest is None:
            return {"status": 501, "error": "Cloud Save not available in mock mode"}

        return await self.ugs_rest.cloud_save_set(key, value)

    @Tool
    async def cloud_save_get(self, ctx: Context, key: str):
        """
        Get a Cloud Save key.
        """
        if self.config.mode != "rest" or self.ugs_rest is None:
            return {"status": 501, "error": "Cloud Save not available in mock mode"}

        return await self.ugs_rest.cloud_save_get(key)

    # -----------------------------------------------------
    # Debug helper
    # -----------------------------------------------------

    def describe(self):
        if self.config.mode == "mock":
            return "TianganMCP(mode=mock)"
        return (
            f"TianganMCP(mode=rest, "
            f"project_id={self.config.project_id}, "
            f"environment_id={self.config.environment_id})"
        )


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------

if __name__ == "__main__":
    config = ServerConfig.from_env()
    server = TianganMCP(config)

    print(server.describe())
    server.run()
