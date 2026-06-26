import ast
import modulefinder
from dataclasses import dataclass, field
from pathlib import Path

from py_to_exe.known_imports import (
    GUI_FRAMEWORKS,
    KNOWN_EXCLUDES,
    KNOWN_HIDDEN_IMPORTS,
)


@dataclass
class AnalysisResult:
    detected_imports: set[str] = field(default_factory=set)
    hidden_imports: list[str] = field(default_factory=list)
    suggested_excludes: list[str] = field(default_factory=list)
    has_gui_framework: bool = False
    warnings: list[str] = field(default_factory=list)


def extract_imports(script_path: Path) -> set[str]:
    try:
        source = script_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = script_path.read_text(encoding="latin-1")

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports


def find_recursive_imports(script_path: Path) -> set[str]:
    finder = modulefinder.ModuleFinder()
    try:
        finder.run_script(str(script_path))
    except Exception:
        return set()
    return {name.split(".")[0] for name in finder.modules}


def analyze(script_path: Path) -> AnalysisResult:
    direct = extract_imports(script_path)

    recursive: set[str] = set()
    try:
        recursive = find_recursive_imports(script_path)
    except Exception:
        pass

    all_imports = direct | recursive

    hidden: list[str] = []
    excludes: list[str] = []
    for pkg in sorted(all_imports):
        if pkg in KNOWN_HIDDEN_IMPORTS:
            hidden.extend(KNOWN_HIDDEN_IMPORTS[pkg])
        if pkg in KNOWN_EXCLUDES:
            excludes.extend(KNOWN_EXCLUDES[pkg])

    has_gui = bool(all_imports & GUI_FRAMEWORKS)

    return AnalysisResult(
        detected_imports=all_imports,
        hidden_imports=hidden,
        suggested_excludes=excludes,
        has_gui_framework=has_gui,
    )
