"""Topological sorter ensuring deterministic linear sequence loads."""

from typing import Dict, List, Set
from app.kernel.exceptions.plugin import PluginValidationError
from app.kernel.plugin.manifest import PluginManifest


class TopologicalSorter:
    """Executes Directed Acyclic Graph calculations parsing installation orders securely."""

    @staticmethod
    def sort_plugins(manifests: List[PluginManifest]) -> List[PluginManifest]:
        """Calculates installation orders while trapping dependency cycles.

        Args:
            manifests: Component schema data matrix references array list.

        Returns:
            List[PluginManifest]: Linearly sorted loading execution list matrix.

        Raises:
            PluginValidationError: If circular reference chains are discovered.
        """
        adjacency: Dict[str, Set[str]] = {}
        lookup: Dict[str, PluginManifest] = {m.name: m for m in manifests}

        for m in manifests:
            adjacency[m.name] = set()
            for dep in m.dependencies:
                if dep.name in lookup:
                    adjacency[m.name].add(dep.name)

        visited: Set[str] = set()
        stack: Set[str] = set()
        order: List[str] = []

        def traverse(name: str) -> None:
            if name in stack:
                raise PluginValidationError(
                    f"Circular reference loop tracked involving component: {name}"
                )
            if name not in visited:
                stack.add(name)
                for dep in adjacency.get(name, set()):
                    traverse(dep)
                stack.remove(name)
                visited.add(name)
                order.append(name)

        for manifest in manifests:
            if manifest.name not in visited:
                traverse(manifest.name)

        return [lookup[name] for name in order]
