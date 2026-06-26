import re
from dataclasses import dataclass


@dataclass
class HumanError:
    title: str
    explanation: str
    fix: str
    original: str


_PATTERNS: list[tuple[re.Pattern[str], callable]] = [
    (
        re.compile(r"ModuleNotFoundError: No module named '(\S+)'"),
        lambda m: HumanError(
            title=f"Missing module: {m.group(1)}",
            explanation=f"Your script imports '{m.group(1)}' but it's not installed.",
            fix=f"pip install {m.group(1)}",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"ImportError: cannot import name '(\S+)' from '(\S+)'"),
        lambda m: HumanError(
            title=f"Cannot import '{m.group(1)}' from '{m.group(2)}'",
            explanation="The module exists but doesn't export this name. Version mismatch likely.",
            fix=f"pip install --upgrade {m.group(2)}",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"FileNotFoundError:.*?['\"]([^'\"]+)['\"]"),
        lambda m: HumanError(
            title=f"File not found: {m.group(1)}",
            explanation="Your script references a file that wasn't included in the package.",
            fix=f"py-to-exe script.py --add-data \"{m.group(1)}:.\"",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"RecursionError|maximum recursion depth"),
        lambda m: HumanError(
            title="Recursion limit hit during analysis",
            explanation="PyInstaller's module analysis went too deep. Happens with heavily nested packages.",
            fix="Try: py-to-exe script.py --hidden-import=<package>  (skip deep analysis)",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"PermissionError:.*?['\"]([^'\"]+)['\"]"),
        lambda m: HumanError(
            title=f"Permission denied: {m.group(1)}",
            explanation="Cannot write to the output directory or a temp file is locked.",
            fix="Close any running instances of your exe, or try a different --output-dir.",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"OSError: \[Errno 28\]|No space left on device"),
        lambda m: HumanError(
            title="Disk full",
            explanation="Not enough disk space to build the executable.",
            fix="Free up disk space and try again.",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"UPX is not available"),
        lambda m: HumanError(
            title="UPX not found (optional)",
            explanation="UPX compresses executables but isn't required.",
            fix="This is just a warning — your build should still succeed.",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"Icon file .* not found"),
        lambda m: HumanError(
            title="Icon file not found",
            explanation="The --icon path doesn't exist or is not a valid .ico file.",
            fix="Check the icon file path. On macOS/Linux, use .png; on Windows, use .ico.",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"Cannot find existing PyInstaller"),
        lambda m: HumanError(
            title="PyInstaller not found",
            explanation="PyInstaller is not installed in the current environment.",
            fix="pip install py-to-exe[pyinstaller]",
            original=m.group(0),
        ),
    ),
    (
        re.compile(r"(?:DLL|shared library).*?not found|cannot open shared object"),
        lambda m: HumanError(
            title="Missing system library",
            explanation="A compiled extension needs a system library that isn't available.",
            fix="On Linux: install the -dev package. On Windows: install Visual C++ Redistributable.",
            original=m.group(0),
        ),
    ),
]


def translate_error(stderr: str) -> HumanError | None:
    for pattern, handler in _PATTERNS:
        match = pattern.search(stderr)
        if match:
            return handler(match)
    return None
