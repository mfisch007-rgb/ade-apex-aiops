"""
Plugin manager.

Coordinates discovery, loading and registration.
"""

from __future__ import annotations

from app.plugins.registry.discovery import PluginDiscovery
from app.plugins.registry.loader import PluginLoader
from app.plugins.registry.registry import PluginRegistry


class PluginManager:
    """
    High-level plugin manager.
    """

    def __init__(self) -> None:
        self.discovery = PluginDiscovery()
        self.loader = PluginLoader()
        self.registry = PluginRegistry()

    def discover(self, directory: str):
        return self.discovery.discover(directory)

    def load(self, module: str):
        plugin = self.loader.load(module)
        self.registry.register(plugin)
        return plugin
