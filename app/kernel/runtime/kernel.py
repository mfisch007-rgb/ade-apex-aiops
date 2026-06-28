"""
ADE-APEX Kernel Runtime implementation.
"""

from __future__ import annotations

from app.kernel.contracts.events import Event, EventResult
from app.kernel.contracts.runtime import RuntimeContract
from app.kernel.runtime.context import RuntimeContext
from app.kernel.runtime.lifecycle import LifecycleManager
from app.kernel.runtime.registry import RuntimeRegistry
from app.kernel.runtime.state import RuntimeState


class KernelRuntime(RuntimeContract):
    """
    Default ADE-APEX runtime.
    """

    VERSION = "1.0.0"

    def __init__(self) -> None:
        self._state = RuntimeState.CREATED
        self.context = RuntimeContext()
        self.registry = RuntimeRegistry()
        self.lifecycle = LifecycleManager()

    @property
    def version(self) -> str:
        return self.VERSION

    @property
    def is_running(self) -> bool:
        return self._state is RuntimeState.RUNNING

    async def initialize(self) -> None:
        self.lifecycle.initialize()
        self._state = RuntimeState.INITIALIZED

    async def start(self) -> None:
        self.lifecycle.start()
        self._state = RuntimeState.RUNNING

    async def stop(self) -> None:
        self.lifecycle.stop()
        self._state = RuntimeState.STOPPED

    async def publish(self, event: Event) -> EventResult:
        return EventResult(
            success=True,
            event_id=event.id,
            message="Event accepted by runtime.",
        )

    async def health(self) -> dict[str, str]:
        return {
            "runtime": self.version,
            "state": self._state.value,
            "status": "healthy",
        }
