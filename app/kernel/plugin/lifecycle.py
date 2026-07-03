"""Plugin lifecycle automation coordinator."""

import logging
from app.kernel.exceptions.plugin import PluginLifecycleError
from app.kernel.plugin.model import PluginInterface, PluginState
from app.kernel.plugin.health import PluginHealth

logger = logging.getLogger("ADE-APEX.PluginLifecycle")


class PluginLifecycleManager:
    """Coordinates runtime operations, validation switches, and execution status states securely."""

    def __init__(self, plugin: PluginInterface, health: PluginHealth) -> None:
        """Initializes state mappings links.

        Args:
            plugin: Target module matching active protocol verification specifications.
            health: Health instrumentation model layer mapping instance metrics.
        """
        self._plugin = plugin
        self._health = health

    async def initialize(self) -> None:
        """Invokes setup pipelines shifting state frameworks safely into position.

        Raises:
            PluginLifecycleError: If operational state changes are invalid.
        """
        if self._health.status not in (
            PluginState.CREATED,
            PluginState.LOADED,
            PluginState.DISCOVERED,
        ):
            raise PluginLifecycleError(
                f"Cannot initialize plugin from status state: {self._health.status.name}"
            )

        try:
            await self._plugin.initialize()
            self._health.transition_state(PluginState.INITIALIZED)
        except Exception as exc:
            self._health.transition_state(PluginState.FAILED)
            self._health.update_execution(success=False, error_msg=str(exc))
            raise PluginLifecycleError(
                f"Plugin initialization lifecycle failed internally: {exc}"
            ) from exc

    async def start(self) -> None:
        """Signals runtime loops shifting initialization frames forward into operation loops."""
        if self._health.status != PluginState.INITIALIZED:
            raise PluginLifecycleError(
                f"Cannot start plugin that is not initialized. Status: {self._health.status.name}"
            )
        self._health.transition_state(PluginState.RUNNING)

    async def shutdown(self) -> None:
        """Gracefully commands target modules to destroy tasks and close resource allocations."""
        if self._health.status == PluginState.STOPPED:
            return

        try:
            await self._plugin.shutdown()
            self._health.transition_state(PluginState.STOPPED)
        except Exception as exc:
            self._health.transition_state(PluginState.FAILED)
            self._health.update_execution(success=False, error_msg=str(exc))
            raise PluginLifecycleError(
                f"Plugin shutdown lifecycle failed internally: {exc}"
            ) from exc

    async def restart(self) -> None:
        """Forces immediate clean shutdowns and cycles execution initialization pipelines."""
        await self.shutdown()
        self._health.status = PluginState.LOADED
        await self.initialize()
        await self.start()

    def enable(self) -> None:
        """Enables target elements out of disabled system statuses blocks."""
        if self._health.status != PluginState.DISABLED:
            raise PluginLifecycleError(
                "Plugin is already active or cannot be transitioned out of disabled state."
            )
        self._health.transition_state(PluginState.LOADED)

    def disable(self) -> None:
        """Halts visibility layers across frameworks tracking runtime components."""
        self._health.transition_state(PluginState.DISABLED)
