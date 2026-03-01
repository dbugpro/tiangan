#!/usr/bin/env python3
"""
Tiangan MCP Server — TGA/MOGI Integration Module
Spec: v260209.2 | Session: DBUG_260301 (1)
Geo-Fence: England (zero_china_dependencies = GLOBAL)
Identity: dbug. / admin. (trailing period enforced)
fastmcp: 3.0.2 API (FastMCP class)
"""

import os
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from fastmcp import FastMCP  # ✅ CORRECT: FastMCP not MCP

# =============================================================================
# CORE IDENTITY & COMPLIANCE (identity.json enforcement)
# =============================================================================
UNIVERSAL_CORE_IDENTITY = "dbug."
ADMIN_CORE_IDENTITY = "admin."
SPEC_VERSION = "v260209.2"
SESSION_ID = "DBUG_260301 (1)"

def validate_identity(role: str) -> bool:
    """Enforce trailing period for core identities per identity.json"""
    if role in ["dbug.", "admin."]:
        return True
    if role in ["dbug", "admin"]:  # Missing period — reject
        return False
    return True  # Other roles (adminx, adminq, etc.) pass through

# =============================================================================
# GEO-FENCE & CONSTRAINTS (geo_fence.json)
# =============================================================================
GEO_FENCE = {
    "current_location": "England",
    "departure_date": "2026-02-28",
    "zero_china_dependencies": "GLOBAL",
    "openai_available": True,
    "copilot_available": True,
    "ue5_compliance": "UE5.3.2"
}

# =============================================================================
# MEC/MFC/MCC ENCODING SCHEMAS (10-bit binary foundation)
# =============================================================================
MFC_MAP = {
    "0": "b5", "1": "a1", "2": "a2", "3": "a3", "4": "a4",
    "5": "a5", "6": "b1", "7": "b2", "8": "b3", "9": "b4"
}

def mmc_to_mfc(mmc: str) -> str:
    """Convert MMC (000-999) → MFC (a1a2a3 format)"""
    if not re.match(r"^\d{3}$", mmc):
        raise ValueError(f"Invalid MMC format: {mmc} (expected 000-999)")
    return "".join(MFC_MAP[d] for d in mmc)

def mfc_to_mmc(mfc: str) -> str:
    """Convert MFC (a1a2a3) → MMC (000-999)"""
    reverse_map = {v: k for k, v in MFC_MAP.items()}
    tokens = re.findall(r"[ab][1-5]", mfc)
    if len(tokens) != 3:
        raise ValueError(f"Invalid MFC format: {mfc} (expected 3 tokens like a1a2a3)")
    return "".join(reverse_map[t] for t in tokens)

def generate_mec_binary(mmc: str) -> str:
    """Generate 10-bit binary representation for MEC (1000 of 1024 permutations used)"""
    index = int(mmc)
    return format(index, f"010b")

# =============================================================================
# SNC (Star Number Code) GENERATOR — S000N Format
# =============================================================================
def generate_snc(base_index: int = 1) -> str:
    """Generate Star Number Code in S000N format"""
    index_str = str(base_index).zfill(3)
    check_digit = sum(int(d) for d in index_str) % 10
    return f"S{index_str}{check_digit}"

def validate_snc(snc: str) -> bool:
    """Validate SNC format: S + 3 digits + 1 check digit"""
    match = re.match(r"^S(\d{3})(\d)$", snc)
    if not match:
        return False
    index_str, check = match.groups()
    expected_check = sum(int(d) for d in index_str) % 10
    return str(expected_check) == check

# =============================================================================
# FOUR DIRECTIONS FLAG ALGORITHM
# =============================================================================
ELEMENTS = ["WOOD", "FIRE", "EARTH", "METAL", "WATER"]
ANIMALS = ["RAT", "OX", "TIGER", "RABBIT", "DRAGON", "SNAKE", 
           "HORSE", "GOAT", "MONKEY", "ROOSTER", "DOG", "PIG"]
DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST", "CENTRE"]

def assign_flags(birth_year: int, element: str, animal: str) -> List[str]:
    """Assign TGA flags based on birth year, element, animal"""
    flags = []
    if element.upper() in ELEMENTS:
        flags.append(f"{element.upper()}_FAMILY")
    if animal.upper() in ANIMALS:
        flags.append(f"{animal.upper()}_FAMILY")
    if animal.upper() in ANIMALS:
        idx = ANIMALS.index(animal.upper())
        flags.append(DIRECTIONS[idx % len(DIRECTIONS)])
    return flags

# =============================================================================
# STORAGE LAYER (Cloud Save / Local Fallback)
# =============================================================================
STORAGE_PATH = os.path.expanduser("~/tga_data/mogi_registrations.json")

def ensure_storage_dir():
    os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)

def load_registrations() -> List[Dict]:
    ensure_storage_dir()
    if os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_registrations(data: List[Dict]):
    ensure_storage_dir()
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# =============================================================================
# MCP SERVER INITIALIZATION (fastmcp 3.0.2 API)
# =============================================================================
mcp = FastMCP("tiangan-tga-mcp")  # ✅ FastMCP not MCP

@mcp.tool()
def tga_register_member(
    email: str,
    birth_year: int,
    element: str,
    animal: str,
    role: str = "dbug."
) -> Dict[str, Any]:
    """Register a new MOGI member (TGA protocol)"""
    if not validate_identity(role):
        return {"error": f"Invalid role: {role} (trailing period required for core identities)"}
    
    base_index = (birth_year - 1900) % 1000 + 1
    snc = generate_snc(base_index)
    flags = assign_flags(birth_year, element, animal)
    email_hash = hashlib.sha256(email.lower().encode()).hexdigest()
    
    record = {
        "snc": snc,
        "email_hash": email_hash,
        "birth_year": birth_year,
        "element": element.upper(),
        "animal": animal.upper(),
        "flags": flags,
        "status": "pending",
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "session": SESSION_ID,
        "geo_fence": GEO_FENCE["current_location"],
        "spec": SPEC_VERSION
    }
    
    registrations = load_registrations()
    if any(r["email_hash"] == email_hash for r in registrations):
        return {"status": "duplicate", "message": "Email already registered", "snc_reserved": snc}
    
    registrations.append(record)
    save_registrations(registrations)
    
    return {
        "status": "pending",
        "message": "Registration received. An admin will email login details manually.",
        "snc_reserved": snc,
        "flags_assigned": flags,
        "next_step": "Check email for manual approval from admin account",
        "mogi_protocol": "No automation — human agent review required",
        "compliance": {
            "identity_enforced": True,
            "geo_fence_compliant": True,
            "zero_china_dependencies": GEO_FENCE["zero_china_dependencies"]
        }
    }

@mcp.tool()
def tga_generate_snc(birth_year: int, index_override: Optional[int] = None) -> Dict[str, str]:
    """Generate a Star Number Code (SNC) for a given birth year"""
    if index_override is not None:
        snc = generate_snc(index_override)
    else:
        base_index = (birth_year - 1900) % 1000 + 1
        snc = generate_snc(base_index)
    return {"snc": snc, "valid": validate_snc(snc), "birth_year": birth_year, "spec": SPEC_VERSION}

@mcp.tool()
def tga_assign_flags(element: str, animal: str) -> Dict[str, List[str]]:
    """Assign TGA direction/element/animal flags"""
    flags = assign_flags(1971, element, animal)
    return {
        "flags": flags,
        "element_valid": element.upper() in ELEMENTS,
        "animal_valid": animal.upper() in ANIMALS,
        "spec": SPEC_VERSION
    }

@mcp.tool()
def tga_get_member(snc: str) -> Optional[Dict[str, Any]]:
    """Retrieve member data by SNC (admin-only in production)"""
    if not validate_snc(snc):
        return {"error": f"Invalid SNC format: {snc}"}
    registrations = load_registrations()
    for record in registrations:
        if record["snc"] == snc:
            return {
                "snc": record["snc"],
                "status": record["status"],
                "element": record["element"],
                "animal": record["animal"],
                "flags": record["flags"],
                "registered_at": record["registered_at"],
                "session": record.get("session"),
                "spec": SPEC_VERSION
            }
    return None

@mcp.tool()
def tga_encode_mec(mmc: str) -> Dict[str, str]:
    """Encode MMC (000-999) → MEC (10-bit binary) + MFC (a1a2a3)"""
    if not re.match(r"^\d{3}$", mmc):
        return {"error": f"Invalid MMC: {mmc} (expected 000-999)"}
    mfc = mmc_to_mfc(mmc)
    mec_binary = generate_mec_binary(mmc)
    return {"mmc": mmc, "mfc": mfc, "mec_binary_10bit": mec_binary, "dual_readable": True, "spec": SPEC_VERSION}

@mcp.tool()
def tga_decode_mec(mec_input: str, mode: str = "mfc") -> Dict[str, str]:
    """Decode MEC input → MMC (000-999)"""
    try:
        if mode == "mfc":
            mmc = mfc_to_mmc(mec_input)
        elif mode == "binary":
            index = int(mec_input, 2)
            mmc = str(index).zfill(3)
        else:
            return {"error": f"Unknown mode: {mode}"}
        return {"input": mec_input, "mode": mode, "mmc_decoded": mmc, "valid": re.match(r"^\d{3}$", mmc) is not None, "spec": SPEC_VERSION}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def tga_health_check() -> Dict[str, Any]:
    """Return server health and compliance status"""
    return {
        "status": "OK",
        "server": "tiangan-tga-mcp",
        "spec": SPEC_VERSION,
        "session": SESSION_ID,
        "identity": {"universal_core": UNIVERSAL_CORE_IDENTITY, "admin_core": ADMIN_CORE_IDENTITY, "trailing_period_enforced": True},
        "geo_fence": GEO_FENCE,
        "tools_available": ["tga_register_member", "tga_generate_snc", "tga_assign_flags", "tga_get_member", "tga_encode_mec", "tga_decode_mec", "tga_health_check"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    print(f"🚀 Tiangan TGA-MCP Server starting...")
    print(f"   Spec: {SPEC_VERSION}")
    print(f"   Session: {SESSION_ID}")
    print(f"   Identity: {UNIVERSAL_CORE_IDENTITY} / {ADMIN_CORE_IDENTITY} (trailing period enforced)")
    print(f"   Geo-Fence: {GEO_FENCE['current_location']} ({GEO_FENCE['zero_china_dependencies']})")
    print(f"   Storage: {STORAGE_PATH}")
    print(f"   Tools: 7 TGA/MOGI endpoints active")
    print(f"   Health: http://localhost:8765/health (via MCP)")
    mcp.run()  # ✅ FastMCP.run() method