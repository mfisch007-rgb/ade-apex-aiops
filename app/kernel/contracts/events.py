"""
Core event contracts for the ADE-APEX platform.

All platform events inherit from these contracts.
No event processing logic belongs here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class EventPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Event:
    """
    Base platform event.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    source: str = ""
    tenant_id: str | None = None
    correlation_id: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: EventPriority = EventPriority.NORMAL
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EventResult:
    """
    Result returned after an event has been processed.
    """

    success: bool
    event_id: str
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
