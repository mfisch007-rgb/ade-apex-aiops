"""
Kernel Runtime contract for the ADE-APEX platform.

Defines the public interface that every Kernel Runtime implementation
must provide. No implementation logic belongs here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.kernel.contracts.events import Event, EventResult


class RuntimeContract(ABC):
    """
    Base contract for the ADE-APEX Kernel Runtime.
    """

    @property
    @abstractmethod
    def version(self) -> str:
        """Current runtime version."""

    @property
    @abstractmethod
    def is_running(self) -> bool:
        """Whether the runtime is active."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the runtime."""

    @abstractmethod
    async def start(self) -> None:
        """Start the runtime."""

    @abstractmethod
    async def stop(self) -> None:
        """Gracefully stop the runtime."""

    @abstractmethod
    async def publish(self, event: Event) -> EventResult:
        """
        Publish an event into the platform.
        """

    @abstractmethod
    async def health(self) -> dict[str, str]:
        """
        Return runtime health information.
        """
