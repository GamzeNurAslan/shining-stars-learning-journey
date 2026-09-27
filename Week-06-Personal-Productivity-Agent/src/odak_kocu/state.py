"""OdakKoçu'nun kalıcı durum yönetimi."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ISTANBUL = ZoneInfo("Europe/Istanbul")
DEFAULT_STATE = {"timer": None, "tasks": [], "routine": [], "sessions": [], "notes": [], "reminders": [], "lists": {}}


def now() -> datetime:
    return datetime.now(ISTANBUL)


class StateStore:
    def __init__(self, path: str | Path = "data/odak-state.json") -> None:
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return json.loads(json.dumps(DEFAULT_STATE))
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        return {**json.loads(json.dumps(DEFAULT_STATE)), **data}

    def save(self, data: dict) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
