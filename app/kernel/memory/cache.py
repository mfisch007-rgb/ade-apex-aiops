"""
Simple runtime cache.
"""

from __future__ import annotations


class MemoryCache:
    """
    In-memory cache.
    """

    def __init__(self) -> None:
        self._cache: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self._cache.get(key)

    def set(self, key: str, value: object) -> None:
        self._cache[key] = value

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
