from click.testing import CliRunner
from py_to_exe.cli import main
from py_to_exe import __version__


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Convert Python scripts" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_no_args():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "py-to-exe" in result.output


def test_doctor_help():
    runner = CliRunner()
    result = runner.invoke(main, ["doctor", "--help"])
    assert result.exit_code == 0
    assert "Check environment" in result.output


def test_doctor_runs():
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert "Python version" in result.output


def test_build_help():
    runner = CliRunner()
    result = runner.invoke(main, ["build", "--help"])
    assert result.exit_code == 0
    assert "Build an executable" in result.output


def test_build_missing_script():
    runner = CliRunner()
    result = runner.invoke(main, ["build", "nonexistent.py"])
    assert result.exit_code != 0


def test_implicit_build_route(tmp_path):
    script = tmp_path / "hello.py"
    script.write_text('print("hi")')
    runner = CliRunner()
    result = runner.invoke(main, [str(script), "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run" in result.output


def test_explicit_build_dry_run(tmp_path):
    script = tmp_path / "hello.py"
    script.write_text('print("hi")')
    runner = CliRunner()
    result = runner.invoke(main, ["build", str(script), "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run" in result.output


def test_unknown_file_as_script():
    runner = CliRunner()
    result = runner.invoke(main, ["totally_not_a_file.py"])
    assert result.exit_code != 0
