"""
Plugin registry for the ADE-APEX platform.

Responsible for registering, discovering and retrieving plugins.
"""

from __future__ import annotations

from app.kernel.contracts.plugin import PluginContract


class PluginRegistry:
    """
    Central plugin registry.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, PluginContract] = {}

    def register(self, plugin: PluginContract) -> None:
        """
        Register a plugin.
        """
        self._plugins[plugin.metadata.name] = plugin

    def unregister(self, name: str) -> None:
        """
        Remove a plugin.
        """
        self._plugins.pop(name, None)

    def get(self, name: str) -> PluginContract | None:
        """
        Retrieve a plugin.
        """
        return self._plugins.get(name)

    def all(self) -> list[PluginContract]:
        """
        Return every registered plugin.
        """
        return list(self._plugins.values())

    def exists(self, name: str) -> bool:
        """
        Check if plugin exists.
        """
        return name in self._plugins
