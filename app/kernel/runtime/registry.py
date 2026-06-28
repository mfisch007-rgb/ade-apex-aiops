"""
Runtime registry.

Maintains platform runtime components.
"""

from __future__ import annotations

from typing import Any


class RuntimeRegistry:
    """
    Registry of runtime services.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a runtime service.
        """
        self._services[name] = service

    def get(self, name: str) -> Any:
        """
        Retrieve a registered service.
        """
        return self._services.get(name)

    def exists(self, name: str) -> bool:
        """
        Check whether a service exists.
        """
        return name in self._services

    def unregister(self, name: str) -> None:
        """
        Remove a service.
        """
        self._services.pop(name, None)

    def clear(self) -> None:
        """
        Remove every registered service.
        """
        self._services.clear()

    @property
    def services(self) -> dict[str, Any]:
        """
        Registered services.
        """
        return dict(self._services)
