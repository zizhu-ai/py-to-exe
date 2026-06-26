from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from py_to_exe import __version__
from py_to_exe.analyzer import analyze
from py_to_exe.output import print_info, print_success

console = Console()


def run_interactive() -> None:
    console.print(f"\n[bold]py-to-exe[/] v{__version__}\n")

    script = _prompt_script()
    if script is None:
        return

    script_path = Path(script)
    console.print()
    print_info("Analyzing dependencies...")
    analysis = analyze(script_path)

    import sys
    stdlib = set(sys.stdlib_module_names) | {"__main__", "builtins"}
    user_imports = {
        m for m in analysis.detected_imports
        if m not in stdlib and not m.startswith("_")
    }
    if user_imports:
        print_success(f"Found imports: {', '.join(sorted(user_imports))}")
    if analysis.hidden_imports:
        pkgs = sorted({h.split(".")[0] for h in analysis.hidden_imports})
        print_success(f"Auto-added hidden imports for: {', '.join(pkgs)}")

    console.print()
    name = Prompt.ask(
        "  Output name",
        default=script_path.stem,
    )

    if analysis.has_gui_framework:
        print_info("GUI framework detected — console will be hidden")
        show_console = False
    else:
        show_console = Confirm.ask("  Show console window?", default=True)

    onefile = Confirm.ask("  Package as single file?", default=False)

    output_dir = Prompt.ask("  Output directory", default="./dist")

    console.print()

    from py_to_exe.core import build

    build(
        script=script,
        engine_preference="auto",
        name=name,
        onefile=onefile,
        console=show_console,
        output_dir=output_dir,
    )


def _prompt_script() -> str | None:
    while True:
        script = Prompt.ask("  Python script to convert")
        script = script.strip().strip("'\"")
        if not script:
            return None
        if Path(script).is_file():
            return script
        console.print(f"  [red]File not found:[/] {script}")
