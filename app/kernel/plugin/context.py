"""Plugin execution isolated execution context framework."""

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass(frozen=True)
class PluginRuntimeContext:
    """Provides immutable environment and localized engine mapping values safely to plugins."""

    environment: str
    global_config: Mapping[str, Any] = field(default_factory=dict)
    state_store: Dict[str, Any] = field(default_factory=dict)

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Extracts configuration elements out of global space safely.

        Args:
            key: Operational lookup route parameter string.
            default: Alternative object parameter reference.

        Returns:
            Any: Target configuration lookup value or fallback value.
        """
        return self.global_config.get(key, default)
