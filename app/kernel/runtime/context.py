"""
Runtime execution context for the ADE-APEX platform.

The RuntimeContext acts as the shared dependency container for the
Kernel Runtime. It owns references to services that are initialized
during startup and made available throughout the platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RuntimeContext:
    """
    Shared runtime context.

    Stores references to platform services without coupling the
    contracts to their implementations.
    """

    services: dict[str, Any] = field(default_factory=dict)

    def register(self, name: str, service: Any) -> None:
        """
        Register a runtime service.
        """
        self.services[name] = service

    def get(self, name: str) -> Any:
        """
        Retrieve a registered runtime service.
        """
        return self.services.get(name)

    def contains(self, name: str) -> bool:
        """
        Determine whether a service exists.
        """
        return name in self.services

    def clear(self) -> None:
        """
        Remove every registered service.
        """
        self.services.clear()
