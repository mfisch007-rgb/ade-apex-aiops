"""
Runtime state definitions for the ADE-APEX platform.
"""

from __future__ import annotations

from enum import Enum


class RuntimeState(str, Enum):
    """
    Lifecycle state of the Kernel Runtime.
    """

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
