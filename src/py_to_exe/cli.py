import click
from py_to_exe import __version__


class DefaultGroup(click.Group):
    """A Click group that falls through to a default handler for unknown commands."""

    def parse_args(self, ctx, args):
        if args and args[0] not in self.commands and not args[0].startswith("-"):
            args = ["build"] + args
        return super().parse_args(ctx, args)


@click.group(cls=DefaultGroup, invoke_without_command=True)
@click.version_option(__version__, "--version")
@click.pass_context
def main(ctx):
    """Convert Python scripts to standalone executables."""
    if ctx.invoked_subcommand is None:
        import sys
        if sys.stdin.isatty():
            from py_to_exe.tui import run_interactive
            run_interactive()
        else:
            click.echo("Run py-to-exe <script.py> to package your script. Use --help for options.")


@main.command()
@click.argument("script", type=click.Path(exists=True))
@click.option("--engine", type=click.Choice(["pyinstaller", "auto"]), default="auto", show_default=True)
@click.option("--name", default=None, help="Output executable name.")
@click.option("--icon", default=None, type=click.Path(), help="Path to icon file.")
@click.option("--onefile", is_flag=True, default=False, help="Bundle into a single file.")
@click.option("--console/--no-console", default=None, help="Show console window (auto-detect if omitted).")
@click.option("--output-dir", "-o", default="./dist", show_default=True, help="Output directory.")
@click.option("--add-data", multiple=True, help="Additional data files (src:dest).")
@click.option("--hidden-import", multiple=True, help="Hidden imports to include.")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable verbose output.")
@click.option("--dry-run", is_flag=True, default=False, help="Show what would be done without running.")
def build(script, engine, name, icon, onefile, console, output_dir, add_data, hidden_import, verbose, dry_run):
    """Build an executable from a Python script."""
    from py_to_exe.core import build as do_build

    result = do_build(
        script=script,
        engine_preference=engine,
        name=name,
        icon=icon,
        onefile=onefile,
        console=console,
        output_dir=output_dir,
        add_data=add_data,
        hidden_import=hidden_import,
        verbose=verbose,
        dry_run=dry_run,
    )
    if result and not result.success:
        raise SystemExit(1)


@main.command()
@click.argument("script", required=False, type=click.Path())
def doctor(script):
    """Check environment and dependencies."""
    from pathlib import Path

    from py_to_exe.doctor import run_checks
    from py_to_exe.output import print_error, print_success, print_warning

    script_path = Path(script) if script else None
    results = run_checks(script_path)

    for r in results:
        if r.passed:
            print_success(f"{r.name}: {r.message}")
        else:
            print_error(f"{r.name}: {r.message}")

    failed = [r for r in results if not r.passed]
    if failed:
        print_warning(f"{len(failed)} issue(s) found. Fix them before building.")
        raise SystemExit(1)
    else:
        print_success("All checks passed!")
