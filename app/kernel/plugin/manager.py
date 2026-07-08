import datetime
import asyncio
from typing import List, Optional
from app.kernel.exceptions.plugin import PluginError
from app.kernel.plugin.event_bus import PluginEventBus
from app.kernel.plugin.event_model import KernelEvent
from app.kernel.plugin.health import PluginHealth
from app.kernel.plugin.lifecycle import PluginLifecycleManager
from app.kernel.plugin.loader import PluginLoader
from app.kernel.plugin.model import PluginInterface
from app.kernel.plugin.registry import PluginRegistry


class PluginManager:
    """Combines registries, dynamic lifecycle managers, and loaders behind unified event-driven APIs."""

    def __init__(self, registry: PluginRegistry, loader: PluginLoader) -> None:
        self.registry = registry
        self._loader = loader
        self._lifecycles: dict[str, PluginLifecycleManager] = {}
        self.event_bus = PluginEventBus()

    async def install_plugin(self, plugin: PluginInterface) -> None:
        """Registers external processing drivers into core registries and publishes lifecycle hooks."""
        health = self._loader.load_instance(plugin)
        self.registry.register(plugin, health)
        self._lifecycles[plugin.metadata.name] = PluginLifecycleManager(plugin, health)

        # Phase 2D Event Hook Implementation
        lifecycle_event = KernelEvent(
            topic="plugin.lifecycle.registered",
            sender="PluginManager",
            payload={
                "plugin_id": plugin.metadata.name,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            },
            timestamp=datetime.datetime.utcnow().isoformat(),
        )
        await self.event_bus.publish(lifecycle_event)

    def install_plugin_sync(self, plugin: PluginInterface) -> None:
        """Legacy sync wrapper for tests and non-async context handlers."""
        asyncio.run(self.install_plugin(plugin))

    def get_lifecycle(self, name: str) -> PluginLifecycleManager:
        """Resolves structural runtime automation handlers safely."""
        manager = self._lifecycles.get(name)
        if not manager:
            raise PluginError(f"Plugin lifecycle lookup failed for: {name}")
        return manager

    def get_plugin_health(self, name: str) -> Optional[PluginHealth]:
        """Queries telemetry properties matching targets."""
        return self.registry.get_health(name)

    def list_installed(self) -> List[PluginInterface]:
        """Lists active installed modules arrays."""
        return self.registry.list_all()
