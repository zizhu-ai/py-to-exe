import sys
from pathlib import Path

from py_to_exe.analyzer import analyze
from py_to_exe.engines import select_engine
from py_to_exe.engines.base import BuildConfig, BuildResult
from py_to_exe.output import print_error, print_info, print_step, print_success

_STDLIB_MODULES: set[str] | None = None


def _get_stdlib_modules() -> set[str]:
    global _STDLIB_MODULES
    if _STDLIB_MODULES is None:
        _STDLIB_MODULES = set(sys.stdlib_module_names)
        _STDLIB_MODULES.update({"__main__", "builtins", "_thread"})
    return _STDLIB_MODULES


def build(
    script: str,
    engine_preference: str = "auto",
    name: str | None = None,
    icon: str | None = None,
    onefile: bool = False,
    console: bool | None = None,
    output_dir: str = "./dist",
    add_data: tuple[str, ...] = (),
    hidden_import: tuple[str, ...] = (),
    verbose: bool = False,
    dry_run: bool = False,
) -> BuildResult | None:
    script_path = Path(script)

    print_step(f"Analyzing {script_path.name}...")
    analysis = analyze(script_path)

    stdlib = _get_stdlib_modules()
    user_imports = {
        m for m in analysis.detected_imports
        if m not in stdlib and not m.startswith("_")
    }
    if user_imports:
        print_info(f"Detected imports: {', '.join(sorted(user_imports))}")

    if analysis.hidden_imports:
        print_info(
            f"Auto-added hidden imports for: "
            f"{', '.join(sorted({h.split('.')[0] for h in analysis.hidden_imports}))}"
        )

    if console is None and analysis.has_gui_framework:
        console = False
        print_info("GUI framework detected → hiding console window")

    engine = select_engine(engine_preference)
    ver = engine.version() or "unknown"
    print_step(f"Using {engine.__class__.__name__} ({ver})")

    all_hidden = list(hidden_import) + analysis.hidden_imports

    parsed_data: list[tuple[str, str]] = []
    for item in add_data:
        if ":" in item:
            src, dest = item.split(":", 1)
            parsed_data.append((src, dest))

    config = BuildConfig(
        script_path=script_path,
        output_dir=Path(output_dir),
        output_name=name,
        onefile=onefile,
        console=console,
        icon=Path(icon) if icon else None,
        hidden_imports=all_hidden,
        add_data=parsed_data,
    )

    if dry_run:
        cmd = engine.get_command_preview(config)
        print_info("Dry run — would execute:")
        print_info(" ".join(cmd))
        return None

    print_step("Building...")

    on_output = None
    if verbose:
        on_output = lambda line: print_info(line)  # noqa: E731

    result = engine.build(config, on_output=on_output)

    if result.success:
        print_success(
            f"Done! Output: {result.output_path} "
            f"({result.elapsed_seconds:.1f}s)"
        )
    else:
        print_error(f"Build failed ({result.elapsed_seconds:.1f}s)")
        from py_to_exe.errors import translate_error

        human = translate_error(result.raw_stderr)
        if human:
            print_error(f"{human.title}")
            print_info(human.explanation)
            print_info(f"Fix: {human.fix}")
        elif result.raw_stderr:
            last_lines = result.raw_stderr.strip().splitlines()[-5:]
            for line in last_lines:
                print_info(line)
        if verbose and result.raw_stderr:
            print_info("--- Full stderr ---")
            for line in result.raw_stderr.strip().splitlines():
                print_info(line)

    return result
