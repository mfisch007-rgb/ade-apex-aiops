"""Central structural lifecycle organizer managing system integrations."""

from typing import List, Optional
from app.kernel.exceptions.plugin import PluginError
from app.kernel.plugin.model import PluginInterface
from app.kernel.plugin.health import PluginHealth
from app.kernel.plugin.registry import PluginRegistry
from app.kernel.plugin.lifecycle import PluginLifecycleManager
from app.kernel.plugin.loader import PluginLoader


class PluginManager:
    """Combines registries, dynamic lifecycle managers, and loaders behind unified APIs."""

    def __init__(self, registry: PluginRegistry, loader: PluginLoader) -> None:
        """Configures execution tracking components.

        Args:
            registry: Central thread-safe runtime object tracking map.
            loader: Subsystem loading code block module validation driver.
        """
        self.registry = registry
        self._loader = loader
        self._lifecycles: dict[str, PluginLifecycleManager] = {}

    def install_plugin(self, plugin: PluginInterface) -> None:
        """Registers external processing drivers into core registries.

        Args:
            plugin: Structural object block conforming to required protocols.
        """
        health = self._loader.load_instance(plugin)
        self.registry.register(plugin, health)
        self._lifecycles[plugin.metadata.name] = PluginLifecycleManager(plugin, health)

    def get_lifecycle(self, name: str) -> PluginLifecycleManager:
        """Resolves structural runtime automation handlers safely matching unique names.

        Args:
            name: Target identification string.

        Returns:
            PluginLifecycleManager: Configured state lifecycle coordinator.

        Raises:
            PluginError: If target module can not be found.
        """
        manager = self._lifecycles.get(name)
        if not manager:
            raise PluginError(f"Plugin lifecycle lookup failed for: {name}")
        return manager

    def get_plugin_health(self, name: str) -> Optional[PluginHealth]:
        """Queries telemetry properties matching targets.

        Args:
            name: Identification string path.

        Returns:
            Optional[PluginHealth]: Configured structural status monitoring block or None.
        """
        return self.registry.get_health(name)

    def list_installed(self) -> List[PluginInterface]:
        """Lists active installed modules arrays.

        Returns:
            List[PluginInterface]: Active modules data block configurations mapping sequence.
        """
        return self.registry.list_all()
