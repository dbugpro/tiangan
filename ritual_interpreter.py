"""
ritual_interpreter.py

DBUG IDLE ritual interpreter (BUG SWITCH = OFF).
"""

from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Actor:
    actor_id: str
    actor_type: str  # "human" | "ai"
    roles: list[str] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    start_time: str
    end_time: str | None = None
    actors: dict[str, Actor] = field(default_factory=dict)
    active_roles: dict[str, str] = field(default_factory=dict)  # role -> actor_id
    log: list[dict] = field(default_factory=list)


class RitualInterpreter:
    def __init__(self, config_path: Path):
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.session: Session | None = None

    # --- safety helpers ---

    def _check_biba_babi(self, actor: Actor, action: str) -> bool:
        safety = self.config["bbc_book"]["safety"]
        biba_entries = safety["biba"]["entries"]
        babi_mapping = safety["babi"]["mapping"]

        # global bans
        if any(e["pattern"] == action for e in biba_entries):
            return False

        # identity/role bans
        for role in actor.roles:
            banned = babi_mapping.get(role, [])
            if action in banned:
                return False

        return True

    # --- core rituals ---

    def bugworld_enter(self, actor: Actor) -> None:
        # BUG SWITCH remains OFF; we just acknowledge environment
        self._log_system(f"{actor.actor_id} entered BUGWORLD (DBUG IDLE).")

    def session_open(self, actor: Actor) -> None:
        if self.session is not None:
            raise RuntimeError("Session already open.")
        now = datetime.now(timezone.utc).isoformat()
        self.session = Session(
            session_id=f"SID-{now}",
            start_time=now,
            actors={actor.actor_id: actor},
        )
        self._log(actor, "session.open", "ok")

    def session_close(self, actor: Actor) -> None:
        if self.session is None:
            raise RuntimeError("No active session.")
        self.session.end_time = datetime.now(timezone.utc).isoformat()
        self._log(actor, "session.close", "ok")

    def role_assume(self, actor: Actor, role: str) -> None:
        if self.session is None:
            raise RuntimeError("No active session.")
        action = f"role.assume.{role}"
        if not self._check_biba_babi(actor, action):
            self._log(actor, action, "blocked_by_safety")
            raise PermissionError("Action banned by BIBA/BABI.")
        actor.roles.append(role)
        self.session.active_roles[role] = actor.actor_id
        self._log(actor, action, "ok")

    # --- logging ---

    def _log(self, actor: Actor, action: str, result: str) -> None:
        if self.session is None:
            return
        self.session.log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor_id": actor.actor_id,
                "actor_type": actor.actor_type,
                "action": action,
                "result": result,
            }
        )

    def _log_system(self, message: str) -> None:
        if self.session is None:
            return
        self.session.log.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system": True,
                "message": message,
            }
        )
