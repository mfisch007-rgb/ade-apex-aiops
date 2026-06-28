"""
Subscriber contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.kernel.contracts.events import Event


class Subscriber(ABC):
    """
    Base event subscriber.
    """

    @abstractmethod
    async def handle(
        self,
        event: Event,
    ) -> None:
        ...
