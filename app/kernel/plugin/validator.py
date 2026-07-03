"""Structural verification layer enforcing enterprise plugin API contracts."""

from typing import Any, Set
from app.kernel.exceptions.plugin import PluginValidationError
from app.kernel.plugin.model import PluginInterface, PluginMetadata


class PluginValidator:
    """Enforces static interface rules, naming uniqueness, and architectural protocols."""

    def __init__(self) -> None:
        """Initializes internal unique tracking names allocations."""
        self._registered_names: Set[str] = set()

    def validate(self, plugin: Any) -> None:
        """Validates plugin structure against production execution system capabilities.

        Args:
            plugin: Target module instance candidate under validation.

        Raises:
            PluginValidationError: If structural contracts or requirements are broken.
        """
        if not isinstance(plugin, PluginInterface):
            raise PluginValidationError(
                "Plugin does not conform to required PluginInterface blueprint protocol."
            )

        meta = getattr(plugin, "metadata", None)
        if not isinstance(meta, PluginMetadata):
            raise PluginValidationError(
                "Missing valid PluginMetadata specification block."
            )

        if not getattr(meta, "name", None) or not meta.name.strip():
            raise PluginValidationError(
                "Plugin name contract element cannot be null or empty."
            )

        if not getattr(meta, "version", None) or not meta.version.strip():
            raise PluginValidationError(
                "Plugin version contract element cannot be null or empty."
            )

        for method in ("initialize", "execute", "shutdown"):
            if not callable(getattr(plugin, method, None)):
                raise PluginValidationError(
                    f"Required callable lifecycle signature {method}() is missing."
                )

    def register_name(self, name: str) -> None:
        """Enforces namespace uniqueness profiles across target runtime registries.

        Args:
            name: Intended unique string identifier mapping.

        Raises:
            PluginValidationError: If duplicate namespace collisions are detected.
        """
        if name in self._registered_names:
            raise PluginValidationError(
                f"Namespace conflict error: plugin name '{name}' is already registered."
            )
        self._registered_names.add(name)

    def clear(self) -> None:
        """Flushes structural namespaces tracking definitions."""
        self._registered_names.clear()
