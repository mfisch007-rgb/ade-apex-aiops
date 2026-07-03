"""Dynamic module plugin loader engine."""

from app.kernel.exceptions.plugin import PluginLoadError, PluginValidationError
from app.kernel.plugin.model import PluginInterface, PluginState, PluginMetadata
from app.kernel.plugin.health import PluginHealth
from app.kernel.plugin.validator import PluginValidator


class PluginLoader:
    """Manages structural validation runs, checking file specifications and dynamic instances."""

    def __init__(self, validator: PluginValidator) -> None:
        """Instantiates structural component tracking hooks.

        Args:
            validator: Production standard engine schema verification layer.
        """
        self._validator = validator

    def load_instance(self, plugin_instance: PluginInterface) -> PluginHealth:
        """Loads and tests a plugin instance against explicit runtime engine blueprints.

        Args:
            plugin_instance: Live runtime instantiation block under verification.

        Returns:
            PluginHealth: Telemetry metric configuration map initialized.

        Raises:
            PluginLoadError: If validation checks fail.
        """
        try:
            self._validator.validate(plugin_instance)
            self._validator.register_name(plugin_instance.metadata.name)
        except PluginValidationError as exc:
            raise PluginLoadError(
                f"Plugin validation failed during load phase: {exc}"
            ) from exc
        except Exception as exc:
            raise PluginLoadError(
                f"Unexpected processing system failure loading target module: {exc}"
            ) from exc

        health = PluginHealth(
            status=PluginState.LOADED, version=plugin_instance.metadata.version
        )
        return health
