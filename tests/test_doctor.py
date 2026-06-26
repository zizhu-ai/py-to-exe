from pathlib import Path

from py_to_exe.doctor import (
    CheckResult,
    check_engine_available,
    check_python_version,
    check_script_syntax,
    check_virtual_env,
    run_checks,
)


def test_check_python_version():
    result = check_python_version()
    assert isinstance(result, CheckResult)
    assert result.passed is True
    assert "3." in result.message


def test_check_virtual_env():
    result = check_virtual_env()
    assert isinstance(result, CheckResult)


def test_check_engine_available():
    result = check_engine_available()
    assert isinstance(result, CheckResult)
    assert result.passed is True
    assert "6." in result.message


def test_check_script_syntax_valid(tmp_path):
    script = tmp_path / "good.py"
    script.write_text('print("hello")\n')
    result = check_script_syntax(script)
    assert result.passed is True


def test_check_script_syntax_invalid(tmp_path):
    script = tmp_path / "bad.py"
    script.write_text("def broken(\n")
    result = check_script_syntax(script)
    assert result.passed is False
    assert "Syntax error" in result.message


def test_check_script_syntax_missing():
    result = check_script_syntax(Path("/nonexistent/script.py"))
    assert result.passed is False
    assert "not found" in result.message.lower()


def test_run_checks_without_script():
    results = run_checks()
    assert len(results) == 3
    assert all(isinstance(r, CheckResult) for r in results)


def test_run_checks_with_script(tmp_path):
    script = tmp_path / "app.py"
    script.write_text("import os\n")
    results = run_checks(script)
    assert len(results) == 4
