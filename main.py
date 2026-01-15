import sys
from src.ui import print_header, console
from src.game import start_game

def main():
    print_header()
    try:
        start_game()
    except KeyboardInterrupt:
        console.print("\n[bold red]Journey interrupted.[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()

