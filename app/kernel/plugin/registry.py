"""Thread-safe registration workspace for plugins and telemetry components."""

import threading
from typing import Dict, List, Optional
from app.kernel.plugin.model import PluginInterface
from app.kernel.plugin.health import PluginHealth


class PluginRegistry:
    """Safe lookup structure containing functional execution drivers and system telemetries."""

    def __init__(self) -> None:
        """Configures atomic recursive execution locks and indexing storage dictionaries."""
        self._lock: threading.RLock = threading.RLock()
        self._plugins: Dict[str, PluginInterface] = {}
        self._health_map: Dict[str, PluginHealth] = {}

    def register(self, plugin: PluginInterface, health: PluginHealth) -> None:
        """Safely saves structural plugin maps alongside tracking performance logs.

        Args:
            plugin: Instantiated plugin implementation component matching interfaces.
            health: Metric collection tracking wrapper interface.
        """
        with self._lock:
            name = plugin.metadata.name
            self._plugins[name] = plugin
            self._health_map[name] = health

    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """Looks up a safe working copy model string mapping paths.

        Args:
            name: Unique route name.

        Returns:
            Optional[PluginInterface]: The matching plugin object or None.
        """
        with self._lock:
            return self._plugins.get(name)

    def get_health(self, name: str) -> Optional[PluginHealth]:
        """Retrieves performance limits safely matching specific targets.

        Args:
            name: Structural name key.

        Returns:
            Optional[PluginHealth]: Target performance monitoring context data or None.
        """
        with self._lock:
            return self._health_map.get(name)

    def list_all(self) -> List[PluginInterface]:
        """Provides an atomic sequence copy of all active running elements.

        Returns:
            List[PluginInterface]: Current operational array elements.
        """
        with self._lock:
            return list(self._plugins.values())
