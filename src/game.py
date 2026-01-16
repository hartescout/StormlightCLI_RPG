import json
import time
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from src.ui import console, print_header
from src.player import Player
from src.persistence import save_game, load_game

def load_orders():
    try:
        with open("src/data/orders.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: src/data/orders.json not found![/bold red]")
        return {}
    except json.JSONDecodeError:
        console.print("[bold red]Error: src/data/orders.json is not valid JSON![/bold red]")
        return {}

def create_character():
    console.print("\n[bold]--- Character Creation ---[/bold]")
    name = Prompt.ask("Enter your Radiant's name", default="Kaladin")
    
    orders = load_orders()
    
    console.print("\nChoose your Order:")
    for order, data in orders.items():
        console.print(f"[bold cyan]{order}[/bold cyan]: {data['description']}")
    
    order_choice = Prompt.ask("Select Order", choices=list(orders.keys()), default="Windrunner")
    
    player = Player(name, order_choice, orders[order_choice])
    console.print(f"\n[bold green]Welcome, {name} of the {order_choice}s![/bold green]")
    time.sleep(1)
    
    from src.prologue import play_prologue
    play_prologue(player)
    
    return player

def camp_menu(player):
    while True:
        print_header()
        console.print(player.status_panel())
        
        console.print("\n[bold]--- Warcamp Menu ---[/bold]")
        console.print("1. [bold yellow]Bridge Run[/bold yellow] (Combat/Loot)")
        console.print("2. Visit Apothecary (Heal/Trade)")
        console.print("3. Talk to Spren (Lore/Advice)")
        console.print("4. [bold blue]Wait for Highstorm[/bold blue]")
        console.print("5. [bold green]Save Game[/bold green]")
        console.print("6. Quit")
        
        choice = IntPrompt.ask("Choose action", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == 1:
            from src.events import start_bridge_run
            result = start_bridge_run(player)
            if not result and player.current_hp <= 0:
                 console.print("[bold red]Game Over.[/bold red]")
                 break
        elif choice == 2:
            from src.shop import visit_shop
            visit_shop(player)
        elif choice == 3:
            from src.dialogue import talk_to_spren
            talk_to_spren(player)
        elif choice == 4:
            from src.highstorm import encounter_highstorm
            result = encounter_highstorm(player)
            if not result:
                console.print("[bold red]Game Over.[/bold red]")
                break
        elif choice == 5:
            save_game(player)
        elif choice == 6:
            return

def start_game():
    console.print("\n[bold]MAIN MENU[/bold]")
    console.print("1. New Game")
    console.print("2. Load Game")
    
    choice = IntPrompt.ask("Choose option", choices=["1", "2"], default="1")
    
    if choice == 2:
        player = load_game()
        if player:
            camp_menu(player)
            return

    player = create_character()
    camp_menu(player)

