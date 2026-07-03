"""Verifies cross-plugin software dependencies matrices."""

from typing import Dict, List
from app.kernel.exceptions.plugin import PluginValidationError
from app.kernel.plugin.manifest import PluginManifest


class PluginDependencyResolver:
    """Checks semantic availability states ensuring operational dependency validation."""

    @staticmethod
    def match_version(version: str, version_range: str) -> bool:
        """Evaluates semantic version rules directly against available version configurations.

        Args:
            version: Live string code version tracking label.
            version_range: Target verification comparison limit specification string.

        Returns:
            bool: Verification truth match confirmation indicators.
        """
        if version_range == "*" or not version_range:
            return True
        if version_range.startswith("=="):
            return version == version_range[2:].strip()
        return version == version_range.strip()

    def resolve_requirements(
        self, manifests: List[PluginManifest]
    ) -> List[PluginManifest]:
        """Verifies existence profiles matching dependency declarations.

        Args:
            manifests: Target set of available configuration profiles.

        Returns:
            List[PluginManifest]: Sequence array containing fully validated elements.

        Raises:
            PluginValidationError: If breaking validation constraints are encountered.
        """
        registry: Dict[str, PluginManifest] = {m.name: m for m in manifests}
        validated: List[PluginManifest] = []

        for manifest in manifests:
            for dep in manifest.dependencies:
                if dep.name not in registry:
                    if dep.optional:
                        continue
                    raise PluginValidationError(
                        f"Unresolved critical dependency: Plugin '{manifest.name}' requires '{dep.name}'."
                    )

                target = registry[dep.name]
                if not self.match_version(target.version, dep.version_range):
                    if dep.optional:
                        continue
                    raise PluginValidationError(
                        f"Version mismatch fault: '{manifest.name}' expects '{dep.name}' range "
                        f"'{dep.version_range}', but found '{target.version}'."
                    )

            validated.append(manifest)

        return validated
