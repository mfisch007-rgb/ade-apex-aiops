"""Plugin operational telemetry tracking layers."""

import time
from dataclasses import dataclass, field
from typing import Optional
from app.kernel.plugin.model import PluginState


@dataclass
class PluginHealth:
    """Mutable structural metric baseline tracker capturing real-time operational limits."""

    status: PluginState = PluginState.CREATED
    uptime: float = 0.0
    last_execution: Optional[float] = None
    execution_count: int = 0
    version: str = "0.0.0"
    last_error: Optional[str] = None
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def transition_state(self, next_state: PluginState) -> None:
        """Transitions execution states, recalculating active uptime configurations safely.

        Args:
            next_state: The target destination lifecycle state.
        """
        self.status = next_state
        if next_state == PluginState.RUNNING:
            if self._start_time is None:
                self._start_time = time.time()
        elif next_state in (
            PluginState.STOPPED,
            PluginState.FAILED,
            PluginState.DISABLED,
        ):
            if self._start_time is not None:
                self.uptime += time.time() - self._start_time
                self._start_time = None

    def update_execution(self, success: bool, error_msg: Optional[str] = None) -> None:
        """Updates invocation count metrics and registers execution failure text maps.

        Args:
            success: Boolean metric indicator showing execution safety.
            error_msg: Failure string details tracking core faults if present.
        """
        now = time.time()
        self.last_execution = now
        self.execution_count += 1
        if not success:
            self.last_error = error_msg
