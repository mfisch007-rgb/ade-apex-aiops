"""
Plugin contracts for the ADE-APEX platform.

Plugins extend the platform with additional capabilities while remaining
isolated from the Kernel implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PluginMetadata:
    """
    Metadata describing a plugin.
    """

    name: str
    version: str
    author: str = ""
    description: str = ""
    enabled: bool = True
    tags: list[str] = field(default_factory=list)


class PluginContract(ABC):
    """
    Base contract implemented by every ADE-APEX plugin.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Plugin metadata."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the plugin."""

    @abstractmethod
    async def execute(
        self,
        action: str,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a plugin action.
        """
