"""Primary execution engine running transaction pipelines through plugins."""

import asyncio
from typing import Any
from app.kernel.exceptions.plugin import PluginExecutionError
from app.kernel.plugin.model import PluginState
from app.kernel.plugin.context import PluginRuntimeContext
from app.kernel.plugin.manager import PluginManager


class PluginRuntime:
    """Dispatches asynchronous processing parameters down into validated plugin spaces."""

    def __init__(self, manager: PluginManager) -> None:
        """Binds internal coordination modules.

        Args:
            manager: Core tracking orchestration layer containing definitions.
        """
        self.manager = manager

    async def execute_plugin(self, name: str, context: PluginRuntimeContext) -> Any:
        """Safely routes processing tasks, tracking diagnostics metrics atomically.

        Args:
            name: Target plugin identification lookup path.
            context: Safe immutable environment reference space values.

        Returns:
            Any: Computation output details returned by target execution blocks.

        Raises:
            PluginExecutionError: If target modules fail inside core calculations.
        """
        plugin = self.manager.registry.get_plugin(name)
        health = self.manager.registry.get_health(name)

        if not plugin or not health:
            raise PluginExecutionError(
                f"Execution target plugin '{name}' is not registered."
            )

        if health.status != PluginState.RUNNING:
            raise PluginExecutionError(
                f"Cannot execute plugin '{name}' because it is in state: {health.status.name}"
            )

        try:
            if asyncio.iscoroutinefunction(plugin.execute):
                result = await plugin.execute(context)
            else:
                result = plugin.execute(context)

            health.update_execution(success=True)
            return result
        except Exception as exc:
            health.update_execution(success=False, error_msg=str(exc))
            raise PluginExecutionError(
                f"Plugin execution loop threw unhandled exception: {exc}"
            ) from exc
