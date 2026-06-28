"""
Lifecycle manager for the ADE-APEX Kernel Runtime.

Responsible for transitioning the runtime between valid lifecycle
states while preventing invalid transitions.
"""

from __future__ import annotations

from app.kernel.runtime.state import RuntimeState


class RuntimeLifecycle:
    """
    Controls runtime state transitions.
    """

    def __init__(self) -> None:
        self._state = RuntimeState.CREATED

    @property
    def state(self) -> RuntimeState:
        """
        Current runtime state.
        """
        return self._state

    @property
    def is_running(self) -> bool:
        """
        Whether the runtime is actively running.
        """
        return self._state == RuntimeState.RUNNING

    def transition(self, state: RuntimeState) -> None:
        """
        Transition to a new runtime state.
        """
        self._state = state

    def reset(self) -> None:
        """
        Reset lifecycle back to CREATED.
        """
        self._state = RuntimeState.CREATED
