import click

from py_to_exe.engines.base import BuildConfig, BuildResult, Engine
from py_to_exe.engines.pyinstaller import PyInstallerEngine

__all__ = ["BuildConfig", "BuildResult", "Engine", "select_engine"]

_ENGINES = {
    "pyinstaller": PyInstallerEngine,
}


def select_engine(preference: str = "auto") -> Engine:
    if preference == "auto":
        engine = PyInstallerEngine()
        if engine.is_available():
            return engine
        raise click.UsageError(
            "No supported build engine found.\n"
            "Install one with: pip install py-to-exe[pyinstaller]"
        )

    if preference not in _ENGINES:
        raise click.UsageError(
            f"Unknown engine '{preference}'. Available: {', '.join(_ENGINES)}"
        )

    engine = _ENGINES[preference]()
    if not engine.is_available():
        raise click.UsageError(
            f"Engine '{preference}' is not installed.\n"
            f"Install with: pip install {preference}"
        )
    return engine
