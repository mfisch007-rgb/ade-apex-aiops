from app.plugins.registry.registry import PluginRegistry


def test_registry_initially_empty():
    registry = PluginRegistry()
    assert registry.all() == []


def test_unregister_missing_plugin():
    registry = PluginRegistry()
    registry.unregister("missing")
    assert registry.all() == []


def test_exists_returns_false():
    registry = PluginRegistry()
    assert registry.exists("missing") is False
