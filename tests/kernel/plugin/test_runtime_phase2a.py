"""Production comprehensive suite validating Phase 2A Plugin Runtime requirements."""

import pytest
import asyncio
from typing import Any
from app.kernel.exceptions.plugin import (
    PluginValidationError,
    PluginLoadError,
    PluginExecutionError,
    PluginLifecycleError,
)
from app.kernel.plugin.model import PluginInterface, PluginMetadata, PluginState
from app.kernel.plugin.context import PluginRuntimeContext
from app.kernel.plugin.health import PluginHealth
from app.kernel.plugin.validator import PluginValidator
from app.kernel.plugin.loader import PluginLoader
from app.kernel.plugin.registry import PluginRegistry
from app.kernel.plugin.lifecycle import PluginLifecycleManager
from app.kernel.plugin.manager import PluginManager
from app.kernel.plugin.runtime import PluginRuntime


class MockValidPlugin:
    """Compliant plugin class matching production specifications perfectly."""

    def __init__(self, name: str = "TestPlugin", version: str = "1.0.0") -> None:
        self.metadata = PluginMetadata(
            name=name,
            version=version,
            description="Enterprise Test Automation Mock Component",
            author="ADE-APEX Core Core Dev",
        )
        self.init_called = False
        self.shutdown_called = False

    async def initialize(self) -> None:
        self.init_called = True

    async def execute(self, context: Any) -> Any:
        return f"Processed context via {self.metadata.name}"

    async def shutdown(self) -> None:
        self.shutdown_called = True


class MockBrokenPlugin:
    """Corrupt plugin component missing interface configuration metrics blocks."""

    def __init__(self) -> None:
        self.metadata = PluginMetadata(
            name="BrokenPlugin",
            version="1.0.0",
            description="Invalid contract structure mock",
            author="Faulty Dev",
        )

    async def initialize(self) -> None:
        pass


@pytest.mark.asyncio
async def test_successful_plugin_lifecycle_and_state_transitions() -> None:
    """Verifies standard state paths matching healthy transitions profiles."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)

    plugin = MockValidPlugin()
    manager.install_plugin(plugin)

    health = manager.get_plugin_health(plugin.metadata.name)
    assert health is not None
    assert health.status == PluginState.LOADED

    lifecycle = manager.get_lifecycle(plugin.metadata.name)
    await lifecycle.initialize()
    assert health.status == PluginState.INITIALIZED
    assert plugin.init_called is True

    await lifecycle.start()
    assert health.status == PluginState.RUNNING

    await lifecycle.shutdown()
    assert health.status == PluginState.STOPPED
    assert plugin.shutdown_called is True


@pytest.mark.asyncio
async def test_plugin_validator_rejects_malformed_contracts() -> None:
    """Checks contract schema validators guard against invalid structures."""
    validator = PluginValidator()
    broken = MockBrokenPlugin()

    with pytest.raises(PluginValidationError):
        validator.validate(broken)


@pytest.mark.asyncio
async def test_loader_prevents_duplicate_namespace_registrations() -> None:
    """Verifies names protection mechanisms filter out naming collisions."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)

    plugin1 = MockValidPlugin(name="UniqueName")
    plugin2 = MockValidPlugin(name="UniqueName")

    manager.install_plugin(plugin1)
    with pytest.raises(PluginLoadError):
        manager.install_plugin(plugin2)


@pytest.mark.asyncio
async def test_runtime_context_integration_and_execution() -> None:
    """Validates execution runs cleanly inside active environments contexts."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)
    runtime = PluginRuntime(manager)

    plugin = MockValidPlugin()
    manager.install_plugin(plugin)

    lifecycle = manager.get_lifecycle(plugin.metadata.name)
    await lifecycle.initialize()
    await lifecycle.start()

    context = PluginRuntimeContext(
        environment="production", global_config={"timeout": 30}
    )
    result = await runtime.execute_plugin(plugin.metadata.name, context)

    assert result == "Processed context via TestPlugin"
    health = manager.get_plugin_health(plugin.metadata.name)
    assert health.execution_count == 1
    assert health.last_execution is not None
    assert health.last_error is None


@pytest.mark.asyncio
async def test_lifecycle_failure_during_initialization() -> None:
    """Verifies failed dynamic components mark error frameworks correctly."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)

    plugin = MockValidPlugin(name="FaultyInitPlugin")

    async def bad_init() -> None:
        raise ValueError("Hardware memory fault simulation.")

    plugin.initialize = bad_init  # type: ignore

    manager.install_plugin(plugin)
    lifecycle = manager.get_lifecycle(plugin.metadata.name)

    with pytest.raises(PluginLifecycleError):
        await lifecycle.initialize()

    health = manager.get_plugin_health(plugin.metadata.name)
    assert health.status == PluginState.FAILED
    assert "Hardware memory fault" in health.last_error


@pytest.mark.asyncio
async def test_runtime_execution_failure_handling() -> None:
    """Ensures errors thrown within task loops are captured safely inside telemetry logs."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)
    runtime = PluginRuntime(manager)

    plugin = MockValidPlugin(name="FaultyExecPlugin")

    async def bad_exec(ctx: Any) -> None:
        raise RuntimeError("Network pipeline timeout.")

    plugin.execute = bad_exec  # type: ignore

    manager.install_plugin(plugin)
    lifecycle = manager.get_lifecycle(plugin.metadata.name)
    await lifecycle.initialize()
    await lifecycle.start()

    context = PluginRuntimeContext(environment="staging")
    with pytest.raises(PluginExecutionError):
        await runtime.execute_plugin(plugin.metadata.name, context)

    health = manager.get_plugin_health(plugin.metadata.name)
    assert health.execution_count == 1
    assert "Network pipeline timeout" in health.last_error


@pytest.mark.asyncio
async def test_enable_disable_lifecycle_state_flows() -> None:
    """Validates toggle states can modify core framework runtime visibility settings."""
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)

    plugin = MockValidPlugin()
    manager.install_plugin(plugin)
    lifecycle = manager.get_lifecycle(plugin.metadata.name)
    health = manager.get_plugin_health(plugin.metadata.name)

    lifecycle.disable()
    assert health.status == PluginState.DISABLED

    lifecycle.enable()
    assert health.status == PluginState.LOADED
