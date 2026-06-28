"""
Plugin discovery for ADE-APEX.

Discovers plugin implementations without loading them.
"""

from __future__ import annotations

from pathlib import Path


class PluginDiscovery:
    """
    Discovers available plugins.
    """

    def discover(self, directory: str) -> list[Path]:
        path = Path(directory)

        if not path.exists():
            return []

        return sorted(path.glob("*.py"))
