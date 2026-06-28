"""
Memory store for ADE-APEX.
"""

from __future__ import annotations

from typing import Any


class MemoryStore:
    """
    Simple in-memory key/value store.

    This becomes replaceable by Redis,
    PostgreSQL,
    Vector DB,
    etc.
    """

    def __init__(self) -> None:
        self._memory: dict[str, Any] = {}

    async def get(self, key: str) -> Any | None:
        return self._memory.get(key)

    async def set(self, key: str, value: Any) -> None:
        self._memory[key] = value

    async def delete(self, key: str) -> None:
        self._memory.pop(key, None)

    async def clear(self) -> None:
        self._memory.clear()
