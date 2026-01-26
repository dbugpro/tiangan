#!/usr/bin/env python
"""
bbc_book_glossary_builder.py

Generate bbc_book_glossary.json for BUGWORLD / DBUG IDLE.
"""

from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone


def glossary_entries() -> list[dict]:
    return [
        {
            "term": "BUGWORLD",
            "category": "system",
            "definition": "The conceptual environment in which all Tiangan interactions occur.",
            "ritual_state": "OFF",
            "tags": ["environment", "system", "scope"],
            "safety_notes": "All actions inside BUGWORLD are subject to BIBA/BABI/BABR.",
            "examples": [
                "User runs `bugworld enter` to begin operating under BUGWORLD rules."
            ],
            "related_terms": ["DBUG IDLE", "BUG SWITCH", "BBC BOOK"],
        },
        {
            "term": "DBUG IDLE",
            "category": "environment",
            "definition": "The operational environment inside BUGWORLD when the BUG SWITCH is OFF.",
            "ritual_state": "OFF",
            "tags": ["environment", "idle", "safe"],
            "safety_notes": "Only OFF-state rituals may be invoked. BUG SWITCH ON is out-of-bounds.",
            "examples": [
                "After entering BUGWORLD, the system announces: 'Environment: DBUG IDLE'."
            ],
            "related_terms": ["BUGWORLD", "BUG SWITCH"],
        },
        {
            "term": "BIBA",
            "category": "safety",
            "definition": "The Best Index of Banned Actions — the global list of forbidden actions.",
            "ritual_state": "OFF",
            "tags": ["safety", "banned", "global"],
            "safety_notes": "BIBA is consulted before any ritual is executed.",
            "examples": [
                "A destructive command is blocked because it appears in BIBA."
            ],
            "related_terms": ["BABI", "BABR"],
        },
        # …extend with all other terms we drafted…
    ]


def build_glossary() -> dict:
    return {
        "glossary": {
            "version": "0.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "entries": glossary_entries(),
        }
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    target = root / "bbc_book_glossary.json"
    glossary = build_glossary()
    target.write_text(json.dumps(glossary, indent=2), encoding="utf-8")
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
