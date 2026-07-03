"""Plugin execution framework error definitions."""


class PluginError(Exception):
    """Base exception for all plugin-related operational failures."""

    pass


class PluginValidationError(PluginError):
    """Raised when a plugin fails structural or contract architectural validation."""

    pass


class PluginLoadError(PluginError):
    """Raised when the plugin dynamic loader fails to initialize target runtime blocks."""

    pass


class PluginExecutionError(PluginError):
    """Raised during live execution failure states within isolated plugins."""

    pass


class PluginLifecycleError(PluginError):
    """Raised during illegal state transitions or corrupt operations in lifecycle managers."""

    pass
