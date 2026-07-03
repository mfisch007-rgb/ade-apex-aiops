from app.plugins.runtime.runtime import PluginRuntime


def test_runtime_initialization():
    runtime = PluginRuntime()

    assert runtime.manager is not None
