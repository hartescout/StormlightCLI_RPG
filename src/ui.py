from rich.console import Console

console = Console()

def print_header():
    console.print("[bold blue]STORMLIGHT ARCHIVE RPG[/bold blue]", justify="center")
    console.print("[italic cyan]Life before death. Strength before weakness. Journey before destination.[/italic cyan]", justify="center")
    console.print("="*40, justify="center")

def print_error(text):
    console.print(f"[bold red]Error:[/bold red] {text}")

def print_success(text):
    console.print(f"[bold green]{text}[/bold green]")
