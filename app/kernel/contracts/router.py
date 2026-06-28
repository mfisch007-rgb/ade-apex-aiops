"""
Router contracts for the ADE-APEX platform.

Routers determine where events, requests, and tasks should
be dispatched across the platform.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.kernel.contracts.events import Event


class RouterContract(ABC):
    """
    Base routing contract.
    """

    @abstractmethod
    async def register(
        self,
        route: str,
        target: Any,
    ) -> None:
        """
        Register a route.
        """

    @abstractmethod
    async def unregister(
        self,
        route: str,
    ) -> None:
        """
        Remove a route.
        """

    @abstractmethod
    async def dispatch(
        self,
        event: Event,
    ) -> Any:
        """
        Dispatch an event to its destination.
        """

    @abstractmethod
    async def resolve(
        self,
        route: str,
    ) -> Any:
        """
        Resolve a registered route.
        """
