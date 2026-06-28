"""
Plugin runtime.

Executes registered plugins.
"""

from __future__ import annotations

from typing import Any

from app.plugins.registry.manager import PluginManager


class PluginRuntime:
    """
    Runtime for executing plugins.
    """

    def __init__(self) -> None:
        self.manager = PluginManager()

    async def execute(
        self,
        module: str,
        action: str,
        **kwargs: Any,
    ) -> Any:
        plugin = self.manager.load(module)

        return await plugin.execute(
            action,
            **kwargs,
        )
