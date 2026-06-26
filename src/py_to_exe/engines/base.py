from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class BuildConfig:
    script_path: Path
    output_dir: Path = field(default_factory=lambda: Path("./dist"))
    output_name: str | None = None
    onefile: bool = False
    console: bool | None = None
    icon: Path | None = None
    hidden_imports: list[str] = field(default_factory=list)
    add_data: list[tuple[str, str]] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)


@dataclass
class BuildResult:
    success: bool
    output_path: Path | None
    engine_name: str
    elapsed_seconds: float
    warnings: list[str] = field(default_factory=list)
    raw_stdout: str = ""
    raw_stderr: str = ""


class Engine(ABC):
    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def version(self) -> str | None: ...

    @abstractmethod
    def build(
        self,
        config: BuildConfig,
        on_output: Callable[[str], None] | None = None,
    ) -> BuildResult: ...

    @abstractmethod
    def get_command_preview(self, config: BuildConfig) -> list[str]: ...
