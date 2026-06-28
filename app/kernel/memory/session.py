"""
Runtime session memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SessionMemory:
    """
    Runtime session storage.
    """

    session_id: str

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any | None:
        return self.values.get(key)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value

    def clear(self) -> None:
        self.values.clear()
