import asyncio
import pytest
from app.kernel.plugin.event_bus import PluginEventBus
from app.kernel.plugin.event_model import KernelEvent


def test_sync_async_bridge_event_bus():
    """Verifies that the Event Bus correctly delivers events inside a controlled runtime loop."""
    bus = PluginEventBus()
    received = []

    def mock_handler(event: KernelEvent):
        received.append(event)

    bus.subscribe("plugin.lifecycle.registered", mock_handler)

    test_event = KernelEvent(
        topic="plugin.lifecycle.registered",
        sender="TestHarness",
        payload={"plugin_id": "core_omnihub"},
        timestamp="2026-07-05T00:00:00",
    )

    # Run the async publish method inside the loop explicitly to avoid silent failure traps
    asyncio.run(bus.publish(test_event))

    assert len(received) == 1
    assert received[0].payload["plugin_id"] == "core_omnihub"
