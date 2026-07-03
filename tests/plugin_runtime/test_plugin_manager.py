from app.plugins.registry.manager import PluginManager


def test_manager_initialization():
    manager = PluginManager()

    assert manager.discovery is not None
    assert manager.loader is not None
    assert manager.registry is not None
