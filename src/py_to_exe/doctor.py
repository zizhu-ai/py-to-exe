import ast
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


def check_python_version() -> CheckResult:
    ver = sys.version_info
    if ver < (3, 10):
        return CheckResult(
            name="Python version",
            passed=False,
            message=f"Python {ver.major}.{ver.minor} detected. Requires 3.10+.",
        )
    return CheckResult(
        name="Python version",
        passed=True,
        message=f"Python {ver.major}.{ver.minor}.{ver.micro}",
    )


def check_virtual_env() -> CheckResult:
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        return CheckResult(
            name="Virtual environment",
            passed=False,
            message=(
                "Not in a virtual environment. "
                "Recommended: create one with 'python -m venv .venv' "
                "to avoid packaging unnecessary system packages."
            ),
        )
    return CheckResult(
        name="Virtual environment",
        passed=True,
        message=f"Active: {sys.prefix}",
    )


def check_engine_available() -> CheckResult:
    try:
        import PyInstaller

        return CheckResult(
            name="PyInstaller",
            passed=True,
            message=f"Version {PyInstaller.__version__}",
        )
    except ImportError:
        return CheckResult(
            name="PyInstaller",
            passed=False,
            message="Not installed. Run: pip install py-to-exe[pyinstaller]",
        )


def check_script_syntax(script_path: Path) -> CheckResult:
    try:
        source = script_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return CheckResult(
            name="Script syntax",
            passed=False,
            message=f"File not found: {script_path.name}",
        )
    except UnicodeDecodeError:
        return CheckResult(
            name="Script syntax",
            passed=False,
            message=f"Cannot read {script_path.name}: encoding error",
        )

    try:
        ast.parse(source)
    except SyntaxError as e:
        return CheckResult(
            name="Script syntax",
            passed=False,
            message=f"Syntax error at line {e.lineno}: {e.msg}",
        )

    return CheckResult(
        name="Script syntax",
        passed=True,
        message=f"{script_path.name} is valid Python",
    )


def run_checks(script_path: Path | None = None) -> list[CheckResult]:
    results = [
        check_python_version(),
        check_virtual_env(),
        check_engine_available(),
    ]
    if script_path:
        results.append(check_script_syntax(script_path))
    return results
