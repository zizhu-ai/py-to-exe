from rich.console import Console

console = Console()


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/] {message}")


def print_error(message: str) -> None:
    console.print(f"[bold red]✗[/] {message}")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]![/] {message}")


def print_info(message: str) -> None:
    console.print(f"[dim]→[/] {message}")


def print_step(message: str) -> None:
    console.print(f"[bold blue]▸[/] {message}")
