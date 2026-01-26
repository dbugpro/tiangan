#!/usr/bin/env python
"""
bbc_book_config_builder.py

Generate bbc_book_config.json for BUGWORLD / DBUG IDLE (BUG SWITCH = OFF).
"""

from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone


def build_config() -> dict:
    return {
        "bbc_book": {
            "version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "environment": {
                "name": "BUGWORLD",
                "mode": "DBUG_IDLE",
                "bug_switch_state": "OFF",
            },
            "session_model": {
                "schema": {
                    "session_id": "string",
                    "start_time": "ISO8601",
                    "end_time": "ISO8601|null",
                    "actors": ["Actor"],
                    "active_roles": ["RoleBinding"],
                    "log": ["LogEntry"],
                    "safety_state": {
                        "biba_version": "int",
                        "babi_version": "int",
                        "babr_version": "int",
                    },
                }
            },
            "actor_model": {
                "schema": {
                    "actor_id": "string",
                    "actor_type": "human|ai",
                    "identities": ["string"],
                    "roles": ["string"],
                }
            },
            "roles": {
                "admina": {
                    "description": "Admin role A",
                    "aliases": [],
                    "secrets_required": True,
                    "allowed_actions": [
                        "session.open",
                        "session.close",
                        "role.assume",
                        "role.release",
                    ],
                    "banned_actions": [],
                },
                "adminb": {
                    "description": "Admin role B",
                    "aliases": [],
                    "secrets_required": True,
                    "allowed_actions": ["session.open", "session.close"],
                    "banned_actions": [],
                },
                "adminc": {
                    "description": "Admin role C",
                    "aliases": [],
                    "secrets_required": True,
                    "allowed_actions": ["session.open"],
                    "banned_actions": [],
                },
                "adminp": {
                    "description": "Primary admin (dbugp)",
                    "aliases": ["dbugp"],
                    "email": "dbug.pro@mail.com",
                    "secrets_required": True,
                    "allowed_actions": [
                        "biba.update",
                        "session.open",
                        "session.close",
                        "config.modify",
                    ],
                    "banned_actions": [],
                },
                "admins": {
                    "description": "Admin role S",
                    "aliases": [],
                    "secrets_required": True,
                    "allowed_actions": ["session.open"],
                    "banned_actions": [],
                },
                "admint": {
                    "description": "Admin role T",
                    "aliases": [],
                    "secrets_required": True,
                    "allowed_actions": ["session.open"],
                    "banned_actions": [],
                },
                "adminx": {
                    "description": "Experimental admin (dbugx)",
                    "aliases": ["dbugx"],
                    "email": "dbugx@mail.com",
                    "secrets_required": True,
                    "allowed_actions": [
                        "session.open",
                        "session.close",
                        "log.annotate",
                    ],
                    "banned_actions": ["biba.update"],
                },
            },
            "safety": {
                "biba": {
                    "version": 1,
                    "entries": [],
                },
                "babi": {
                    "version": 1,
                    "mapping": {},
                },
                "babr": {
                    "version": 1,
                    "patterns": [],
                },
            },
        }
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    target = root / "bbc_book_config.json"
    config = build_config()
    target.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
