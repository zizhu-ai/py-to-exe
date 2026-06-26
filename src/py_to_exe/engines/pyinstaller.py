import subprocess
import sys
import time
from typing import Callable

from py_to_exe.engines.base import BuildConfig, BuildResult, Engine


class PyInstallerEngine(Engine):
    def is_available(self) -> bool:
        try:
            import PyInstaller  # noqa: F401

            return True
        except ImportError:
            return False

    def version(self) -> str | None:
        try:
            import PyInstaller

            return PyInstaller.__version__
        except ImportError:
            return None

    def _build_command(self, config: BuildConfig) -> list[str]:
        cmd = [sys.executable, "-m", "PyInstaller"]

        if config.onefile:
            cmd.append("--onefile")

        if config.console is True:
            cmd.append("--console")
        elif config.console is False:
            cmd.append("--windowed")

        if config.output_name:
            from pathlib import PurePosixPath, PureWindowsPath

            name = config.output_name
            if (
                "/" in name
                or "\\" in name
                or ".." in PurePosixPath(name).parts
                or ".." in PureWindowsPath(name).parts
            ):
                raise ValueError(
                    f"Invalid output name '{name}': must not contain path separators or '..'"
                )
            cmd.extend(["--name", name])

        if config.icon:
            cmd.extend(["--icon", str(config.icon)])

        cmd.extend(["--distpath", str(config.output_dir)])
        cmd.extend(["--specpath", str(config.output_dir)])
        cmd.extend(["--workpath", str(config.output_dir / "build")])

        for mod in config.hidden_imports:
            cmd.append(f"--hidden-import={mod}")

        for src, dest in config.add_data:
            cmd.append(f"--add-data={src}:{dest}")

        cmd.extend(["--noconfirm", "--clean"])
        cmd.extend(config.extra_args)
        cmd.append(str(config.script_path))

        return cmd

    def get_command_preview(self, config: BuildConfig) -> list[str]:
        return self._build_command(config)

    def build(
        self,
        config: BuildConfig,
        on_output: Callable[[str], None] | None = None,
    ) -> BuildResult:
        cmd = self._build_command(config)
        start = time.time()

        if on_output:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout_lines: list[str] = []
            assert proc.stdout is not None
            for line in proc.stdout:
                stdout_lines.append(line)
                on_output(line.rstrip("\n"))
            assert proc.stderr is not None
            stderr = proc.stderr.read()
            proc.wait()
            stdout = "".join(stdout_lines)
            returncode = proc.returncode
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
            stdout = result.stdout
            stderr = result.stderr
            returncode = result.returncode

        elapsed = time.time() - start
        name = config.output_name or config.script_path.stem

        if config.onefile:
            output_path = config.output_dir / name
        else:
            output_path = config.output_dir / name / name

        return BuildResult(
            success=returncode == 0,
            output_path=output_path if returncode == 0 else None,
            engine_name="pyinstaller",
            elapsed_seconds=round(elapsed, 2),
            raw_stdout=stdout,
            raw_stderr=stderr,
        )
