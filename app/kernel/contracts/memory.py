"""
Memory contracts for the ADE-APEX platform.

Defines the interface for all memory providers used by the Kernel,
including short-term, long-term and vector memories.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MemoryRecord:
    """
    Represents a single memory item.
    """

    key: str
    value: Any
    namespace: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)


class MemoryContract(ABC):
    """
    Base interface implemented by every ADE-APEX memory provider.
    """

    @abstractmethod
    async def get(self, key: str) -> MemoryRecord | None:
        """Retrieve a memory record."""

    @abstractmethod
    async def set(self, record: MemoryRecord) -> None:
        """Store a memory record."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a memory record."""

    @abstractmethod
    async def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[MemoryRecord]:
        """
        Search memory records.
        """
