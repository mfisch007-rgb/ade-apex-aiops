"""
ADE-APEX Event Bus.

Central asynchronous event dispatcher.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Awaitable, Callable

from app.kernel.contracts.events import Event

EventHandler = Callable[[Event], Awaitable[None]]


class EventBus:
    """
    In-process asynchronous event bus.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        handler: EventHandler,
    ) -> None:
        self._subscribers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        for handler in self._subscribers.get(event.event_type, []):
            await handler(event)

    def clear(self) -> None:
        self._subscribers.clear()
