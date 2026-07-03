"""Plugin manifest verification models and structural immutable schemas."""

from dataclasses import dataclass, field
from typing import List, Mapping


@dataclass(frozen=True)
class PluginDependencySpec:
    """Immutable declaration requirement specifications binding an external plugin constraint."""

    name: str
    version_range: str
    optional: bool = False


@dataclass(frozen=True)
class PluginManifest:
    """Immutable data schema containing the structurally checked properties of a discovered plugin."""

    name: str
    version: str
    entry_point: str
    description: str
    author: str
    dependencies: List[PluginDependencySpec] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    metadata_options: Mapping[str, str] = field(default_factory=dict)
