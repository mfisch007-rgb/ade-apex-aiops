"""Plugin runtime state and manifest models."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Protocol, runtime_checkable


class PluginState(Enum):
    """Execution status states defining the precise lifetime boundaries of a plugin."""

    CREATED = auto()
    DISCOVERED = auto()
    LOADED = auto()
    INITIALIZED = auto()
    RUNNING = auto()
    STOPPED = auto()
    FAILED = auto()
    DISABLED = auto()


@dataclass(frozen=True)
class PluginMetadata:
    """Immutable structural manifest specification for enterprise plugins."""

    name: str
    version: str
    description: str
    author: str


@runtime_checkable
class PluginInterface(Protocol):
    """Structural interface standard defining runtime-compliant plugins."""

    metadata: PluginMetadata

    async def initialize(self) -> None:
        """Execute async startup dependencies allocation blocks."""
        ...

    async def execute(self, context: Any) -> Any:
        """Run isolated pipeline computations against runtime execution engines."""
        ...

    async def shutdown(self) -> None:
        """Gracefully release external processing allocations and worker queues."""
        ...
