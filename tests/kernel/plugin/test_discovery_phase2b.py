"""Production validation suite checking structural Phase 2B Discovery implementation."""

import json
import pathlib
import pytest
from app.kernel.exceptions.plugin import PluginValidationError
from app.kernel.plugin.manifest import PluginManifest, PluginDependencySpec
from app.kernel.plugin.parser import PluginManifestParser
from app.kernel.plugin.scanner import PluginScanner
from app.kernel.plugin.dependency import PluginDependencyResolver
from app.kernel.plugin.topology import TopologicalSorter


def test_parser_with_valid_manifest() -> None:
    """Verifies that a well-formed JSON string is correctly parsed into a PluginManifest."""
    raw_json = """{
        "name": "core_ledger",
        "version": "1.4.2",
        "entry_point": "app.plugins.ledger.Engine",
        "description": "Enterprise Ledger Core",
        "author": "ADE-APEX Engineering",
        "dependencies": [
            {"name": "payment_gateway", "version_range": "==2.0.0", "optional": false}
        ],
        "capabilities": ["accounting", "ledger_flow"],
        "metadata_options": {"isolation_level": "strict"}
    }"""
    manifest = PluginManifestParser.parse_json(raw_json)
    assert manifest.name == "core_ledger"
    assert manifest.version == "1.4.2"
    assert len(manifest.dependencies) == 1
    assert manifest.dependencies[0].name == "payment_gateway"
    assert manifest.dependencies[0].optional is False


def test_parser_invalid_json_throws_validation_error() -> None:
    """Ensures that poorly structured syntax triggers a validation failure response."""
    bad_json = "{ 'name': 'broken', malformed_json: true "
    with pytest.raises(PluginValidationError):
        PluginManifestParser.parse_json(bad_json)


def test_parser_missing_keys_throws_validation_error() -> None:
    """Ensures that missing required fields inside raw schemas raises validation errors."""
    incomplete_json = """{
        "name": "incomplete_plugin",
        "version": "1.0.0"
    }"""
    with pytest.raises(PluginValidationError) as exc:
        PluginManifestParser.parse_json(incomplete_json)
    assert "Missing required manifest elements" in str(exc.value)


def test_scanner_extracts_manifest_from_directory(tmp_path: pathlib.Path) -> None:
    """Verifies filesystem navigation parsing runs correctly across target folders."""
    plugin_dir = tmp_path / "mock_plugin"
    plugin_dir.mkdir()
    manifest_file = plugin_dir / "manifest.json"

    valid_data = {
        "name": "mock_plugin",
        "version": "1.0.0",
        "entry_point": "main.Plugin",
        "description": "Mock automated workspace tool",
        "author": "Dev",
    }
    manifest_file.write_text(json.dumps(valid_data), encoding="utf-8")

    parser = PluginManifestParser()
    scanner = PluginScanner(parser)
    results = scanner.scan_directory(tmp_path)

    assert len(results) == 1
    assert plugin_dir in results
    assert results[plugin_dir].name == "mock_plugin"


def test_resolver_handles_missing_critical_dependency() -> None:
    """Checks that missing non-optional dependencies trigger resolution failure blocks."""
    manifest = PluginManifest(
        name="A",
        version="1.0.0",
        entry_point="ep",
        description="d",
        author="a",
        dependencies=[PluginDependencySpec(name="B", version_range="*")],
    )
    resolver = PluginDependencyResolver()
    with pytest.raises(PluginValidationError) as exc:
        resolver.resolve_requirements([manifest])
    assert "Unresolved critical dependency" in str(exc.value)


def test_resolver_allows_missing_optional_dependency() -> None:
    """Ensures that missing dependencies marked optional do not interrupt loading runs."""
    manifest = PluginManifest(
        name="A",
        version="1.0.0",
        entry_point="ep",
        description="d",
        author="a",
        dependencies=[PluginDependencySpec(name="B", version_range="*", optional=True)],
    )
    resolver = PluginDependencyResolver()
    results = resolver.resolve_requirements([manifest])
    assert len(results) == 1


def test_topological_sorting_resolves_linear_order() -> None:
    """Validates that installation arrays match explicit requirement hierarchies."""
    manifest_b = PluginManifest(
        name="B", version="1.0.0", entry_point="ep", description="d", author="a"
    )
    manifest_a = PluginManifest(
        name="A",
        version="1.0.0",
        entry_point="ep",
        description="d",
        author="a",
        dependencies=[PluginDependencySpec(name="B", version_range="*")],
    )

    sorted_output = TopologicalSorter.sort_plugins([manifest_a, manifest_b])
    assert len(sorted_output) == 2
    assert sorted_output[0].name == "B"
    assert sorted_output[1].name == "A"


def test_topological_sorting_detects_cycles() -> None:
    """Verifies that dependency loop cycles throw explicit validation exceptions."""
    manifest_a = PluginManifest(
        name="A",
        version="1.0.0",
        entry_point="ep",
        description="d",
        author="a",
        dependencies=[PluginDependencySpec(name="B", version_range="*")],
    )
    manifest_b = PluginManifest(
        name="B",
        version="1.0.0",
        entry_point="ep",
        description="d",
        author="a",
        dependencies=[PluginDependencySpec(name="A", version_range="*")],
    )

    with pytest.raises(PluginValidationError) as exc:
        TopologicalSorter.sort_plugins([manifest_a, manifest_b])
    assert "Circular reference loop tracked" in str(exc.value)
