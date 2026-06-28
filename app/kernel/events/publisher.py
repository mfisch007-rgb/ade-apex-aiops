"""
Publisher contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.kernel.contracts.events import Event


class Publisher(ABC):
    """
    Base publisher.
    """

    @abstractmethod
    async def publish(
        self,
        event: Event,
    ) -> None:
        ...
