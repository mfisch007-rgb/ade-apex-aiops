from pathlib import Path
from tempfile import TemporaryDirectory

from app.plugins.registry.discovery import PluginDiscovery


def test_empty_directory():
    with TemporaryDirectory() as tmp:
        discovery = PluginDiscovery()
        plugins = discovery.discover(tmp)
        assert plugins == []


def test_discovers_python_files():
    with TemporaryDirectory() as tmp:
        p = Path(tmp)

        (p / "plugin_one.py").write_text("# plugin")
        (p / "plugin_two.py").write_text("# plugin")
        (p / "README.md").write_text("ignore")

        discovery = PluginDiscovery()
        plugins = discovery.discover(tmp)

        assert len(plugins) == 2
        assert all(x.suffix == ".py" for x in plugins)
