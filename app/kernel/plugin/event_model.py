"""Event definitions and payload contracts for the enterprise plugin subsystem."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class KernelEvent:
    """Immutable event payload container transmitted across the system event bus fabric."""

    topic: str
    sender: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
