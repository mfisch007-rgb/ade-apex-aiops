"""
Agent contracts for the ADE-APEX platform.

Agents are intelligent execution units responsible for processing work,
interacting with the Kernel Runtime, and collaborating through events.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.kernel.contracts.events import Event


@dataclass(slots=True)
class AgentMetadata:
    """
    Metadata describing an agent.
    """

    name: str
    version: str
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    enabled: bool = True


class AgentContract(ABC):
    """
    Base contract implemented by every ADE-APEX agent.
    """

    @property
    @abstractmethod
    def metadata(self) -> AgentMetadata:
        """Agent metadata."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the agent."""

    @abstractmethod
    async def handle(self, event: Event) -> Any:
        """
        Handle a platform event.
        """

    @abstractmethod
    async def health(self) -> dict[str, Any]:
        """
        Return current health information.
        """
