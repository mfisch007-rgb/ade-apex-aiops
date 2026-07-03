"""Filesystem workspace directory scanner for dynamic plugin bundle exploration."""

import pathlib
from typing import Dict
from app.kernel.exceptions.plugin import PluginLoadError
from app.kernel.plugin.manifest import PluginManifest
from app.kernel.plugin.parser import PluginManifestParser


class PluginScanner:
    """Traverses local system workspace directory targets to extract isolated plugin manifests."""

    def __init__(self, parser: PluginManifestParser) -> None:
        """Initializes scanner instance with manifest configuration parsing drivers.

        Args:
            parser: Target manifest structure verification engine instance.
        """
        self._parser = parser

    def scan_directory(
        self, base_path: pathlib.Path
    ) -> Dict[pathlib.Path, PluginManifest]:
        """Traverses directories checking path locations for manifest profiles.

        Args:
            base_path: Main directory root location path object to scan.

        Returns:
            Dict[pathlib.Path, PluginManifest]: Map linking file path locations to extracted manifests.

        Raises:
            PluginLoadError: If directory navigation actions fail.
        """
        discovered: Dict[pathlib.Path, PluginManifest] = {}

        if not base_path.exists():
            return discovered

        if not base_path.is_dir():
            raise PluginLoadError(
                f"Target system workspace boundary path is not a directory structure: {base_path}"
            )

        try:
            for manifest_file in base_path.glob("**/manifest.json"):
                try:
                    content = manifest_file.read_text(encoding="utf-8")
                    manifest = self._parser.parse_json(content)
                    discovered[manifest_file.parent] = manifest
                except Exception as exc:
                    raise PluginLoadError(
                        f"Failed to extract manifest definition at {manifest_file}: {exc}"
                    ) from exc
        except Exception as exc:
            if not isinstance(exc, PluginLoadError):
                raise PluginLoadError(
                    f"Directory scanner tree mapping exploration failed: {exc}"
                ) from exc
            raise exc

        return discovered
