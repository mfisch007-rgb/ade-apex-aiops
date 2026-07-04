"""Synchronous/Asynchronous thread-safe event bus broker execution engine."""

import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, Set
from app.kernel.plugin.event_model import KernelEvent

logger = logging.getLogger("ADE-APEX.EventBus")


class PluginEventBus:
    """Enterprise event broker managing registrations and isolated asynchronous topic dispatches."""

    def __init__(self) -> None:
        """Initializes subject topic registration matrices."""
        self._listeners: Dict[str, Set[Callable[[KernelEvent], Any]]] = {}

    def subscribe(self, topic: str, handler: Callable[[KernelEvent], Any]) -> None:
        """Registers a handler callable to receive event dispatches for a specific topic.

        Args:
            topic: Target message routing pattern string.
            handler: Callable callback logic tracking structural execution targets.
        """
        if topic not in self._listeners:
            self._listeners[topic] = set()
        self._listeners[topic].add(handler)

    def unsubscribe(self, topic: str, handler: Callable[[KernelEvent], Any]) -> None:
        """Removes an active handler registration mapping allocation safely.

        Args:
            topic: Explicit message route channel match string.
            handler: Previously configured callback method block.
        """
        if topic in self._listeners and handler in self._listeners[topic]:
            self._listeners[topic].remove(handler)
            if not self._listeners[topic]:
                del self._listeners[topic]

    async def publish(self, event: KernelEvent) -> None:
        """Asynchronously dispatches an event frame out to all topic subscription listeners.

        Args:
            event: Immutable transaction context record under current transmission.
        """
        handlers = self._listeners.get(event.topic, set()).copy()
        if not handlers:
            return

        tasks = [self._safe_execute_handler(handler, event) for handler in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_execute_handler(
        self, handler: Callable[[KernelEvent], Any], event: KernelEvent
    ) -> None:
        """Protects event cycle dispatches against unhandled handler loop error faults.

        Args:
            handler: Processing component function boundary target block.
            event: Core contextual details payload data frame.
        """
        try:
            if inspect.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as exc:
            logger.error(
                f"EventBus route processing error encountered inside handler {handler.__name__}: {exc}"
            )
