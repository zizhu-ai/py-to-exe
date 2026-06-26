from pathlib import Path

import click
import pytest

from py_to_exe.engines import select_engine
from py_to_exe.engines.base import BuildConfig
from py_to_exe.engines.pyinstaller import PyInstallerEngine


@pytest.fixture
def engine():
    return PyInstallerEngine()


@pytest.fixture
def sample_config(tmp_path):
    script = tmp_path / "app.py"
    script.write_text('print("hello")')
    return BuildConfig(script_path=script, output_dir=tmp_path / "dist")


def test_pyinstaller_is_available(engine):
    result = engine.is_available()
    assert isinstance(result, bool)


def test_pyinstaller_version(engine):
    if engine.is_available():
        ver = engine.version()
        assert ver is not None
        assert isinstance(ver, str)
        assert len(ver) > 0


def test_build_config_defaults():
    cfg = BuildConfig(script_path=Path("test.py"))
    assert cfg.onefile is False
    assert cfg.console is None
    assert cfg.output_dir == Path("./dist")
    assert cfg.hidden_imports == []
    assert cfg.add_data == []
    assert cfg.output_name is None


def test_command_preview(engine, sample_config):
    cmd = engine.get_command_preview(sample_config)
    assert "PyInstaller" in " ".join(cmd)
    assert str(sample_config.script_path) in cmd
    assert "--noconfirm" in cmd
    assert "--clean" in cmd


def test_command_preview_onefile(engine, sample_config):
    sample_config.onefile = True
    cmd = engine.get_command_preview(sample_config)
    assert "--onefile" in cmd


def test_command_preview_hidden_imports(engine, sample_config):
    sample_config.hidden_imports = ["foo", "bar"]
    cmd = engine.get_command_preview(sample_config)
    assert "--hidden-import=foo" in cmd
    assert "--hidden-import=bar" in cmd


def test_command_preview_windowed(engine, sample_config):
    sample_config.console = False
    cmd = engine.get_command_preview(sample_config)
    assert "--windowed" in cmd


def test_command_preview_console_none(engine, sample_config):
    sample_config.console = None
    cmd = engine.get_command_preview(sample_config)
    assert "--console" not in cmd
    assert "--windowed" not in cmd


def test_select_engine_auto():
    try:
        engine = select_engine("auto")
        assert isinstance(engine, PyInstallerEngine)
    except SystemExit:
        pytest.skip("No engine available")


def test_select_engine_invalid():
    with pytest.raises(click.UsageError):
        select_engine("nuitka")


def test_command_preview_includes_specpath(engine, sample_config):
    cmd = engine.get_command_preview(sample_config)
    assert "--specpath" in " ".join(cmd)
    assert "--workpath" in " ".join(cmd)


def test_name_path_traversal_rejected(engine, sample_config):
    sample_config.output_name = "../escape"
    with pytest.raises(ValueError, match="path separators"):
        engine.get_command_preview(sample_config)


def test_name_with_slash_rejected(engine, sample_config):
    sample_config.output_name = "foo/bar"
    with pytest.raises(ValueError, match="path separators"):
        engine.get_command_preview(sample_config)


def test_name_simple_accepted(engine, sample_config):
    sample_config.output_name = "my-app"
    cmd = engine.get_command_preview(sample_config)
    assert "--name" in cmd
    assert "my-app" in cmd


def test_build_with_mock_subprocess(engine, sample_config, monkeypatch):
    import subprocess

    calls = []

    def mock_run(cmd, **kwargs):
        calls.append(cmd)

        class FakeResult:
            stdout = "BUILD SUCCESSFUL"
            stderr = ""
            returncode = 0

        return FakeResult()

    monkeypatch.setattr(subprocess, "run", mock_run)
    result = engine.build(sample_config)
    assert result.success is True
    assert result.engine_name == "pyinstaller"
    assert len(calls) == 1
    assert "PyInstaller" in " ".join(calls[0])


def test_build_failure_with_mock(engine, sample_config, monkeypatch):
    import subprocess

    def mock_run(cmd, **kwargs):
        class FakeResult:
            stdout = ""
            stderr = "ModuleNotFoundError: No module named 'missing_pkg'"
            returncode = 1

        return FakeResult()

    monkeypatch.setattr(subprocess, "run", mock_run)
    result = engine.build(sample_config)
    assert result.success is False
    assert result.output_path is None
    assert "missing_pkg" in result.raw_stderr


def test_build_with_on_output_callback(engine, sample_config, monkeypatch):
    import subprocess

    lines_received = []

    class FakeProc:
        stdout = iter(["line1\n", "line2\n"])
        stderr = type("FakeStderr", (), {"read": lambda self: ""})()
        returncode = 0

        def wait(self):
            pass

    monkeypatch.setattr(subprocess, "Popen", lambda cmd, **kw: FakeProc())
    result = engine.build(sample_config, on_output=lambda line: lines_received.append(line))
    assert result.success is True
    assert lines_received == ["line1", "line2"]
