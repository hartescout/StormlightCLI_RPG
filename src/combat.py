import json
import random
import time
from rich.prompt import Prompt
from src.ui import console, print_header

def load_enemies():
    with open("src/data/enemies.json", "r") as f:
        return json.load(f)

def combat_encounter(player):
    enemies_data = load_enemies()
    enemy_name = random.choice(list(enemies_data.keys()))
    stats = enemies_data[enemy_name]
    
    enemy = {
        "name": enemy_name,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "damage": stats["damage"],
        "loot": stats["loot_spheres"],
        "xp": stats.get("xp", 20)
    }
    
    console.print(f"\n[bold red]COMBAT STARTED![/bold red]")
    console.print(f"You faced a [bold orange1]{enemy['name']}[/bold orange1]!")
    time.sleep(1)
    
    # Combat flags
    enemy_stunned = False
    player_dodging = False
    
    while player.current_hp > 0 and enemy["hp"] > 0:
        print_header()
        console.print(player.status_panel())
        console.print(f"\n[bold orange1]{enemy['name']}[/bold orange1]: {enemy['hp']}/{enemy['max_hp']} HP")
        if enemy_stunned:
            console.print("[bold yellow]Enemy is STUNNED![/bold yellow]")
        if player_dodging:
            console.print("[bold blue]You are obscured by illusions (High Dodge Chance)[/bold blue]")
        
        console.print("\n[bold]Actions:[/bold]")
        console.print("1. [bold]Attack[/bold] (Physical)")
        console.print("2. [bold cyan]Heal[/bold cyan] (5 Stormlight -> 10 HP)")
        console.print("3. [bold magenta]Surge[/bold magenta] (Cast specific Order ability)")
        console.print("4. [dim]Flee[/dim]")
        
        action = Prompt.ask("Choose action", choices=["1", "2", "3", "4"], default="1")
        
        # Reset turn flags
        player_turn_done = False
        
        # Player Actions
        if action == "1":
            base_dmg = random.randint(8, 12)
            total_dmg = base_dmg + player.damage_bonus
            enemy["hp"] -= total_dmg
            console.print(f"You struck the {enemy['name']} for [bold green]{total_dmg}[/bold green] damage!")
            player_turn_done = True
            
        elif action == "2":
            if player.heal():
                console.print("[cyan]Stormlight mends your wounds...[/cyan]")
                player_turn_done = True
            else:
                console.print("[dim]Not enough Stormlight or already full HP![/dim]")
                
        elif action == "3":
            # SURGE MENU
            console.print(f"\n[bold magenta]--- {player.order} Surges ---[/bold magenta]")
            if player.order == "Windrunner":
                console.print("1. [bold]Basic Lashing[/bold] (10 Light) - High Gravity Dmg")
                console.print("2. [bold]Full Lashing[/bold] (15 Light) - Bind Enemy (Stun)")
            elif player.order == "Lightweaver":
                console.print("1. [bold]Illumination[/bold] (5 Light) - Create Decoy (Dodge Buff)")
                console.print("2. [bold]Soulcast[/bold] (20 Light) - Transform Enemy (Massive Dmg)")
            
            console.print("B. Back")
            surge_choice = Prompt.ask("Cast Surge", choices=["1", "2", "B"], default="1")
            
            if surge_choice == "B":
                continue # Go back to main loop without ending turn
            
            # Windrunner Logic
            if player.order == "Windrunner":
                if surge_choice == "1": # Basic Lashing
                    if player.current_stormlight >= 10:
                        player.current_stormlight -= 10
                        dmg = random.randint(20, 35)
                        enemy["hp"] -= dmg
                        console.print(f"You lash the {enemy['name']} to the ceiling! It falls for [bold cyan]{dmg}[/bold cyan] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Full Lashing
                    if player.current_stormlight >= 15:
                        player.current_stormlight -= 15
                        enemy_stunned = True
                        console.print(f"You infuse the ground with Stormlight. The {enemy['name']} is [bold yellow]stuck[/bold yellow]!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

            # Lightweaver Logic
            elif player.order == "Lightweaver":
                if surge_choice == "1": # Illumination
                    if player.current_stormlight >= 5:
                        player.current_stormlight -= 5
                        player_dodging = True
                        console.print("You weave an illusion of yourself. The enemy is confused!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Soulcast
                    if player.current_stormlight >= 20:
                        player.current_stormlight -= 20
                        dmg = random.randint(40, 60)
                        enemy["hp"] -= dmg
                        console.print(f"You Soulcast the air into fire around the {enemy['name']}! [bold magenta]{dmg}[/bold magenta] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

        elif action == "4":
            console.print("You run back to the bridge...")
            return False
            
        time.sleep(1)
        
        if not player_turn_done:
            continue # If they went back or failed a cast, don't let enemy attack
        
        # Enemy Turn
        if enemy["hp"] > 0:
            if enemy_stunned:
                console.print(f"The {enemy['name']} struggles against the Lashing but cannot move!")
                enemy_stunned = False # Stun lasts 1 turn
            else:
                # Dodge Check
                hit_chance = 50 if player_dodging else 100
                if random.randint(1, 100) <= hit_chance:
                    dmg = random.randint(stats["damage"]-2, stats["damage"]+2)
                    player.current_hp -= dmg
                    console.print(f"The {enemy['name']} hits you for [bold red]{dmg}[/bold red] damage!")
                else:
                    console.print(f"The {enemy['name']} attacks your illusion! [bold green]Miss![/bold green]")
                
                player_dodging = False # Dodge lasts 1 turn
            
            time.sleep(1)
            
    if player.current_hp <= 0:
        console.print("\n[bold red]YOU HAVE DIED.[/bold red]")
        console.print("Your sphere fades...")
        return False
    else:
        console.print(f"\n[bold green]VICTORY![/bold green]")
        console.print(f"You found {enemy['loot']} spheres on the body.")
        player.spheres += enemy['loot']
        player.gain_xp(enemy['xp'])
        
        # Stormlight recharge chance
        recharge = random.randint(0, 10)
        if recharge > 0:
            actual = player.breathe_stormlight(recharge)
            console.print(f"You drew [cyan]{actual} Stormlight[/cyan] from nearby gems.")
            
        Prompt.ask("\n[dim]Press Enter to return to camp...[/dim]")
        return True