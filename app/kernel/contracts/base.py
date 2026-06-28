"""
Base contracts used across the ADE-APEX platform.

Everything in the platform derives from these contracts.
Business logic must never live here.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class Contract:
    """
    Root immutable contract.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)


class Component(ABC):
    """
    Base interface implemented by every platform component.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    async def initialize(self) -> None:
        """
        Called during platform startup.
        """

    async def shutdown(self) -> None:
        """
        Called during graceful shutdown.
        """


class Serializable(ABC):
    """
    Common serialization interface.
    """

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
