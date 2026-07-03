import pytest

from app.plugins.registry.loader import PluginLoader


def test_load_standard_library_module():
    loader = PluginLoader()
    module = loader.load("json")
    assert module.__name__ == "json"


def test_load_missing_module():
    loader = PluginLoader()

    with pytest.raises(ModuleNotFoundError):
        loader.load("ade_apex_missing_plugin")
