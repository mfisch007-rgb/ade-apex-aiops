"""
Plugin loader for ADE-APEX.

Responsible for importing plugin modules.
"""

from __future__ import annotations

import importlib


class PluginLoader:
    """
    Loads plugin modules.
    """

    def load(self, module: str):
        return importlib.import_module(module)
