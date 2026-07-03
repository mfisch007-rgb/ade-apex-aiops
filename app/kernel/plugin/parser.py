"""Plugin manifest structure verification parser."""

import json
from typing import Any, Dict, List
from app.kernel.exceptions.plugin import PluginValidationError
from app.kernel.plugin.manifest import PluginDependencySpec, PluginManifest


class PluginManifestParser:
    """Parses raw text data inputs into validated structural PluginManifest objects."""

    @staticmethod
    def parse_json(raw_content: str) -> PluginManifest:
        """Parses a raw JSON text string into a typed, validated PluginManifest object.

        Args:
            raw_content: Raw JSON text read from a manifest file.

        Returns:
            PluginManifest: A valid immutable manifest structure.

        Raises:
            PluginValidationError: If structural rules or parameters are invalid.
        """
        if not raw_content.strip():
            raise PluginValidationError(
                "Manifest content is empty and cannot be processed."
            )

        try:
            data: Dict[str, Any] = json.loads(raw_content)
        except json.JSONDecodeError as err:
            raise PluginValidationError(
                f"Invalid JSON format configuration syntax: {err}"
            ) from err

        required_keys = {"name", "version", "entry_point", "description", "author"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            raise PluginValidationError(
                f"Missing required manifest elements: {', '.join(missing_keys)}"
            )

        for key in required_keys:
            if not isinstance(data[key], str) or not data[key].strip():
                raise PluginValidationError(
                    f"Manifest attribute '{key}' must be a non-empty string reference."
                )

        dependencies: List[PluginDependencySpec] = []
        if "dependencies" in data:
            if not isinstance(data["dependencies"], list):
                raise PluginValidationError(
                    "The 'dependencies' parameter must be configured as a structured list."
                )

            for index, dep in enumerate(data["dependencies"]):
                if not isinstance(dep, dict):
                    raise PluginValidationError(
                        f"Dependency specification index {index} must be a dictionary block."
                    )
                if "name" not in dep or "version_range" not in dep:
                    raise PluginValidationError(
                        f"Dependency specs at index {index} must contain 'name' and 'version_range'."
                    )

                dependencies.append(
                    PluginDependencySpec(
                        name=str(dep["name"]),
                        version_range=str(dep["version_range"]),
                        optional=bool(dep.get("optional", False)),
                    )
                )

        capabilities = [str(cap) for cap in data.get("capabilities", [])]
        metadata_options = {
            str(k): str(v) for k, v in data.get("metadata_options", {}).items()
        }

        return PluginManifest(
            name=data["name"],
            version=data["version"],
            entry_point=data["entry_point"],
            description=data["description"],
            author=data["author"],
            dependencies=dependencies,
            capabilities=capabilities,
            metadata_options=metadata_options,
        )
