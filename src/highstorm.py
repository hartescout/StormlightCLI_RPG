import random
import time
from rich.prompt import Prompt
from src.ui import console, print_header

def encounter_highstorm(player):
    print_header()
    console.print("\n[bold on black] THE HIGHSTORM COMES [/bold on black]", justify="center")
    console.print("\nThe sky turns black. The Stormfather approaches. The winds scream like dying gods.")
    time.sleep(1)
    
    console.print("\n[bold]What will you do?[/bold]")
    console.print("1. [green]Secure spheres and hide[/green] (Safe, gain Currency)")
    console.print("2. [red]Step into the storm[/red] (Danger, maximize Stormlight)")
    
    choice = Prompt.ask("Choose action", choices=["1", "2"])
    
    if choice == "1":
        console.print("\nYou huddle in the barracks, listening to the destruction outside...")
        time.sleep(2)
        found_spheres = random.randint(5, 15)
        player.spheres += found_spheres
        console.print(f"[bold green]The storm passes.[/bold green] You collect {found_spheres} infused spheres washed up by the rain.")
    
    elif choice == "2":
        console.print("\nYou step out. The wind threatens to flay the skin from your bones!")
        time.sleep(1)
        
        # Risk calculation
        damage = random.randint(10, 50)
        console.print(f"Debris strikes you! You take [bold red]{damage}[/bold red] damage.")
        player.current_hp -= damage
        
        if player.current_hp <= 0:
            console.print("[bold dark_red]The Stormfather showed no mercy.[/bold dark_red]")
            return False # Died
        
        console.print("\n[bold cyan]LIGHT![/bold cyan]")
        console.print("The Stormlight floods your veins. You are bursting with power!")
        player.current_stormlight = player.max_stormlight
        console.print("[italic]You feel renewed.[/italic]")

    time.sleep(1)
    return True # Survived
