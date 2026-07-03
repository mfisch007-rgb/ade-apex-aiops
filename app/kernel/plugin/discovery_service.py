"""Orchestrator integrating scanner, parser, resolver, and topological sorting mechanisms."""

import pathlib
from typing import List
from app.kernel.exceptions.plugin import PluginLoadError
from app.kernel.plugin.manifest import PluginManifest
from app.kernel.plugin.scanner import PluginScanner
from app.kernel.plugin.dependency import PluginDependencyResolver
from app.kernel.plugin.topology import TopologicalSorter


class PluginDiscoveryService:
    """Discovers, parses, resolves, and topologically sorts plugins from the filesystem."""

    def __init__(
        self,
        scanner: PluginScanner,
        resolver: PluginDependencyResolver,
        sorter: TopologicalSorter,
    ) -> None:
        """Initializes the discovery service with pipeline dependencies.

        Args:
            scanner: Filesystem explorer component.
            resolver: Semantic dependency requirement checker.
            sorter: Dependency graph linear execution sorter.
        """
        self._scanner = scanner
        self._resolver = resolver
        self._sorter = sorter

    def discover_and_sort(self, base_path: pathlib.Path) -> List[PluginManifest]:
        """Runs the entire discovery pipeline from root scan to ordered manifests output.

        Args:
            base_path: Main folder destination search target to process.

        Returns:
            List[PluginManifest]: Topologically ordered valid plugin manifests.

        Raises:
            PluginLoadError: If any underlying phase fails or encounters errors.
        """
        try:
            discovered_map = self._scanner.scan_directory(base_path)
            manifest_list = list(discovered_map.values())
            validated_manifests = self._resolver.resolve_requirements(manifest_list)
            sorted_manifests = self._sorter.sort_plugins(validated_manifests)
            return sorted_manifests
        except Exception as exc:
            if isinstance(exc, PluginLoadError):
                raise exc
            raise PluginLoadError(
                f"Plugin discovery pipeline failed processing directory layout: {exc}"
            ) from exc
