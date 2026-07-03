"""Production integration testing suite validating pipeline interactions from Phase 2B to Phase 2A."""

import json
import pathlib
import pytest
from typing import Any
from app.kernel.exceptions.plugin import PluginLoadError
from app.kernel.plugin.model import PluginMetadata, PluginState
from app.kernel.plugin.context import PluginRuntimeContext
from app.kernel.plugin.validator import PluginValidator
from app.kernel.plugin.loader import PluginLoader
from app.kernel.plugin.registry import PluginRegistry
from app.kernel.plugin.manager import PluginManager
from app.kernel.plugin.runtime import PluginRuntime
from app.kernel.plugin.parser import PluginManifestParser
from app.kernel.plugin.scanner import PluginScanner
from app.kernel.plugin.dependency import PluginDependencyResolver
from app.kernel.plugin.topology import TopologicalSorter
from app.kernel.plugin.discovery_service import PluginDiscoveryService


class DynamicDiscoveredMockPlugin:
    """Mock instantiation target dynamically reflecting values parsed from physical discovery steps."""

    def __init__(self, name: str, version: str) -> None:
        self.metadata = PluginMetadata(
            name=name,
            version=version,
            description="Integration Runtime Test Mock Instance",
            author="ADE-APEX System Engineering Core",
        )
        self.initialized = False
        self.executed = False
        self.shutdown_completed = False

    async def initialize(self) -> None:
        self.initialized = True

    async def execute(self, context: Any) -> Any:
        self.executed = True
        return f"Execution success for custom module: {self.metadata.name}"

    async def shutdown(self) -> None:
        self.shutdown_completed = True


@pytest.mark.asyncio
async def test_end_to_end_discovery_to_runtime_pipeline_execution(
    tmp_path: pathlib.Path,
) -> None:
    """Validates full architecture sequence traversing exploration to running stages."""
    # 1. Setup physical workspace mock modules setup
    plugin_a_dir = tmp_path / "plugin_alpha"
    plugin_b_dir = tmp_path / "plugin_beta"
    plugin_a_dir.mkdir()
    plugin_b_dir.mkdir()

    manifest_a = {
        "name": "plugin_alpha",
        "version": "2.1.0",
        "entry_point": "app.plugins.Alpha",
        "description": "Alpha service",
        "author": "Core Engine",
        "dependencies": [{"name": "plugin_beta", "version_range": "1.0.0"}],
    }
    manifest_b = {
        "name": "plugin_beta",
        "version": "1.0.0",
        "entry_point": "app.plugins.Beta",
        "description": "Beta low-level driver dependency",
        "author": "System Support Core",
    }

    (plugin_a_dir / "manifest.json").write_text(
        json.dumps(manifest_a), encoding="utf-8"
    )
    (plugin_b_dir / "manifest.json").write_text(
        json.dumps(manifest_b), encoding="utf-8"
    )

    # 2. Instantiate all discovery tools
    parser = PluginManifestParser()
    scanner = PluginScanner(parser)
    resolver = PluginDependencyResolver()
    sorter = TopologicalSorter()
    discovery_service = PluginDiscoveryService(scanner, resolver, sorter)

    # 3. Instantiate Phase 2A components
    validator = PluginValidator()
    loader = PluginLoader(validator)
    registry = PluginRegistry()
    manager = PluginManager(registry, loader)
    runtime = PluginRuntime(manager)

    # 4. Execute Discovery Run
    ordered_manifests = discovery_service.discover_and_sort(tmp_path)
    assert len(ordered_manifests) == 2
    assert ordered_manifests[0].name == "plugin_beta"
    assert ordered_manifests[1].name == "plugin_alpha"

    # 5. Dynamically load mock plugin instances based on discovery orders
    instances = {
        "plugin_beta": DynamicDiscoveredMockPlugin("plugin_beta", "1.0.0"),
        "plugin_alpha": DynamicDiscoveredMockPlugin("plugin_alpha", "2.1.0"),
    }

    for manifest in ordered_manifests:
        plugin_instance = instances[manifest.name]
        manager.install_plugin(plugin_instance)

    # 6. Verify managers and registries track elements perfectly
    installed_list = manager.list_installed()
    assert len(installed_list) == 2

    alpha_health = manager.get_plugin_health("plugin_alpha")
    beta_health = manager.get_plugin_health("plugin_beta")
    assert alpha_health is not None and beta_health is not None
    assert alpha_health.status == PluginState.LOADED
    assert beta_health.status == PluginState.LOADED

    # 7. Advance structures sequentially forward into operational scopes
    for manifest in ordered_manifests:
        lifecycle = manager.get_lifecycle(manifest.name)
        await lifecycle.initialize()
        await lifecycle.start()

    assert alpha_health.status == PluginState.RUNNING
    assert beta_health.status == PluginState.RUNNING

    # 8. Fire execution tasks checks
    context = PluginRuntimeContext(environment="production")
    result_beta = await runtime.execute_plugin("plugin_beta", context)
    result_alpha = await runtime.execute_plugin("plugin_alpha", context)

    assert result_beta == "Execution success for custom module: plugin_beta"
    assert result_alpha == "Execution success for custom module: plugin_alpha"
    assert beta_health.execution_count == 1
    assert alpha_health.execution_count == 1


@pytest.mark.asyncio
async def test_pipeline_breaks_on_discovery_exception(tmp_path: pathlib.Path) -> None:
    """Ensures discovery service routes errors correctly up into management layers."""
    corrupt_dir = tmp_path / "corrupt_plugin"
    corrupt_dir.mkdir()
    (corrupt_dir / "manifest.json").write_text(
        "{ malformed json string ", encoding="utf-8"
    )

    parser = PluginManifestParser()
    scanner = PluginScanner(parser)
    resolver = PluginDependencyResolver()
    sorter = TopologicalSorter()
    discovery_service = PluginDiscoveryService(scanner, resolver, sorter)

    with pytest.raises(PluginLoadError):
        discovery_service.discover_and_sort(tmp_path)
