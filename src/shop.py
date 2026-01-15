from rich.prompt import Prompt, IntPrompt
from src.ui import console, print_header, print_error, print_success
import time

def visit_shop(player):
    while True:
        print_header()
        console.print(player.status_panel())
        console.print("\n[bold]--- The Apothecary ---[/bold]")
        console.print("[italic]An old ardent looks up from mixing herbs.[/italic]")
        console.print(f"You have [bold yellow]{player.spheres} spheres[/bold yellow].")
        
        console.print("\n1. [bold green]Bandages[/bold green] (5 spheres) - Heals 20 HP")
        console.print("2. [bold cyan]Infused Chip[/bold cyan] (10 spheres) - Restores 10 Stormlight")
        console.print("3. [bold red]Sharpen Weapon[/bold red] (50 spheres) - +2 Damage (Permanent)")
        console.print("4. Leave")
        
        choice = IntPrompt.ask("What do you need?", choices=["1", "2", "3", "4"])
        
        if choice == 1:
            if player.spheres >= 5:
                if player.current_hp < player.max_hp:
                    player.spheres -= 5
                    player.current_hp = min(player.max_hp, player.current_hp + 20)
                    print_success("You apply the bandages. Wounds close.")
                else:
                    console.print("You are already healthy.")
            else:
                print_error("Not enough spheres.")
        
        elif choice == 2:
            if player.spheres >= 10:
                if player.current_stormlight < player.max_stormlight:
                    player.spheres -= 10
                    player.current_stormlight = min(player.max_stormlight, player.current_stormlight + 10)
                    print_success("You breathe in the Light.")
                else:
                    console.print("You cannot hold more Stormlight.")
            else:
                print_error("Not enough spheres.")
                
        elif choice == 3:
            if player.spheres >= 50:
                player.spheres -= 50
                # We need a way to track weapon damage. For now, we'll hack it into the player object or inventory.
                # Let's add a simple damage_bonus attribute to player if it doesn't exist.
                if not hasattr(player, 'damage_bonus'):
                    player.damage_bonus = 0
                player.damage_bonus += 2
                print_success("Your weapon is honed to a razor edge.")
            else:
                print_error("Not enough spheres.")
        
        elif choice == 4:
            break
            
        time.sleep(1)
