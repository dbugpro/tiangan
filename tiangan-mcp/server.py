import os
import base64
import asyncio
import json
import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

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
            if not project_id: missing.append("UNITY_PROJECT_ID")
            if not environment_id: missing.append("UNITY_ENVIRONMENT_ID")
            if not api_key: missing.append("UNITY_API_KEY")
            if missing:
                raise ValueError(f"MCP_MODE=rest but missing required env vars: {', '.join(missing)}")

        return cls(mode=mode, project_id=project_id, environment_id=environment_id, api_key=api_key)


# ---------------------------------------------------------
# TGA/MOGI Logic Helpers
# ---------------------------------------------------------

class TGAMogiEngine:
    """Handles SNC generation, Flag assignment, and MOGI registration logic."""
    
    # Simple in-memory store for demo (replace with Redis/DB in production)
    _members: Dict[str, dict] = {}
    _next_snc_id: int = 0

    @staticmethod
    def generate_snc() -> str:
        """Generate next Star Number Code (S000N format)."""
        current_id = TGAMogiEngine._next_snc_id
        TGAMogiEngine._next_snc_id += 1
        
        if current_id < 10000:
            return f"S000{current_id}"
        elif current_id < 100000:
            return f"S0000{current_id}"
        else:
            return f"S{current_id}"

    @staticmethod
    def assign_flags(element: str, animal: str, birth_year: int) -> List[str]:
        """Assign flags based on Element, Animal, and invented Direction logic."""
        flags = []
        if element: flags.append(f"{element.upper()}_FAMILY")
        if animal: flags.append(f"{animal.upper()}_FAMILY")
        
        # Simple Direction Invention Logic (Modulo 4 of Birth Year)
        directions = ["NORTH_SECTOR", "EAST_SECTOR", "SOUTH_SECTOR", "WEST_SECTOR"]
        dir_index = birth_year % 4
        flags.append(directions[dir_index])
        
        return flags

    @classmethod
    def register_member(cls, email: str, birth_year: int, element: str, animal: str) -> dict:
        """Register a new MOGI member."""
        snc = cls.generate_snc()
        flags = cls.assign_flags(element, animal, birth_year)
        
        member_data = {
            "snc": snc,
            "email": email,
            "birth_year": birth_year,
            "element": element,
            "animal": animal,
            "flags": flags,
            "status": "PENDING_MANUAL_APPROVAL",
            "registered_at": datetime.now().isoformat(),
            "protocol": "MOGI_MANUAL_REGISTRATION"
        }
        
        cls._members[snc] = member_data
        return member_data


# ---------------------------------------------------------
# MCP Server
# ---------------------------------------------------------

class TianganMCP(MCP):
    def __init__(self, config: ServerConfig):
        super().__init__(name="tiangan-mcp")
        self.config = config
        self.mock_cloud_code = MockCloudCodeClient()
        self.ugs_rest = None
        if config.mode == "rest":
            self.ugs_rest = UGSRestClient(
                project_id=config.project_id,
                environment_id=config.environment_id,
                api_key=config.api_key,
            )

        # Register Existing Tools
        self.register_tool(self.run_cloud_code)
        self.register_tool(self.cloud_save_set)
        self.register_tool(self.cloud_save_get)

        # Register NEW TGA/MOGI Tools
        self.register_tool(self.tga_register_member)
        self.register_tool(self.tga_generate_snc)
        self.register_tool(self.tga_assign_flags)
        self.register_tool(self.tga_get_member)

    # --- Existing UGS Tools ---

    @Tool
    async def run_cloud_code(self, ctx: Context, script_name: str, params: dict):
        return await self.mock_cloud_code.run_script(script_name, params)

    @Tool
    async def cloud_save_set(self, ctx: Context, key: str, value: dict):
        if self.config.mode != "rest" or self.ugs_rest is None:
            return {"status": 501, "error": "Cloud Save not available in mock mode"}
        return await self.ugs_rest.cloud_save_set(key, value)

    @Tool
    async def cloud_save_get(self, ctx: Context, key: str):
        if self.config.mode != "rest" or self.ugs_rest is None:
            return {"status": 501, "error": "Cloud Save not available in mock mode"}
        return await self.ugs_rest.cloud_save_get(key)

    # --- NEW TGA/MOGI Tools ---

    @Tool
    async def tga_register_member(self, ctx: Context, email: str, birth_year: int, element: str, animal: str):
        """
        Register a new member via MOGI protocol (Manual Registration).
        Returns: SNC, Flags, and Status.
        """
        try:
            result = TGAMogiEngine.register_member(email, birth_year, element, animal)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @Tool
    async def tga_generate_snc(self, ctx: Context):
        """Generate the next available Star Number Code (S000N)."""
        snc = TGAMogiEngine.generate_snc()
        return {"status": "success", "snc": snc}

    @Tool
    async def tga_assign_flags(self, ctx: Context, element: str, animal: str, birth_year: int):
        """Assign Family and Direction flags based on birth data."""
        flags = TGAMogiEngine.assign_flags(element, animal, birth_year)
        return {"status": "success", "flags": flags}

    @Tool
    async def tga_get_member(self, ctx: Context, snc: str):
        """Retrieve member details by SNC."""
        member = TGAMogiEngine._members.get(snc)
        if member:
            return {"status": "success", "data": member}
        return {"status": "error", "message": "Member not found"}

    def describe(self):
        if self.config.mode == "mock":
            return "TianganMCP(mode=mock) [TGA/MOGI Enabled]"
        return f"TianganMCP(mode=rest, project={self.config.project_id}) [TGA/MOGI Enabled]"


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------

if __name__ == "__main__":
    config = ServerConfig.from_env()
    server = TianganMCP(config)
    print(server.describe())
    server.run()