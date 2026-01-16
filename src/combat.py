import json
import random
import time
from rich.prompt import Prompt
from src.ui import console, print_header

def load_enemies():
    try:
        with open("src/data/enemies.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: src/data/enemies.json not found![/bold red]")
        return {}
    except json.JSONDecodeError:
        console.print("[bold red]Error: src/data/enemies.json is not valid JSON![/bold red]")
        return {}

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
        
        action = Prompt.ask("Choose action", choices=["1", "2", "3", "4"])
        
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
                console.print("2. [bold]Full Lashing[/bold] (20 Light) - Bind Enemy (Stun)")
            elif player.order == "Lightweaver":
                console.print("1. [bold]Illumination[/bold] (8 Light) - Create Decoy (Dodge Buff)")
                console.print("2. [bold]Soulcast[/bold] (25 Light) - Transform Enemy (Massive Dmg)")
            elif player.order == "Skybreaker":
                console.print("1. [bold]Gravity Lashing[/bold] (12 Light) - Crush Enemy")
                console.print("2. [bold]Division[/bold] (18 Light) - Split Enemy Apart (High Dmg)")
            elif player.order == "Edgedancer":
                console.print("1. [bold]Friction Slide[/bold] (6 Light) - Evade (Dodge Buff)")
                console.print("2. [bold]Regrowth[/bold] (15 Light) - Heal Self (30 HP)")
            elif player.order == "Elsecaller":
                console.print("1. [bold]Soulcast[/bold] (20 Light) - Transform Matter (Dmg)")
                console.print("2. [bold]Elsecall[/bold] (30 Light) - Teleport Strike (Massive Dmg)")

            console.print("B. Back")
            surge_choice = Prompt.ask("Cast Surge", choices=["1", "2", "B"])
            
            if surge_choice == "B":
                continue # Go back to main loop without ending turn
            
            # Windrunner Logic
            if player.order == "Windrunner":
                if surge_choice == "1": # Basic Lashing
                    if player.current_stormlight >= 10:
                        player.current_stormlight -= 10
                        dmg = random.randint(15, 25)
                        enemy["hp"] -= dmg
                        console.print(f"You lash the {enemy['name']} to the ceiling! It falls for [bold cyan]{dmg}[/bold cyan] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Full Lashing
                    if player.current_stormlight >= 20:
                        player.current_stormlight -= 20
                        enemy_stunned = True
                        console.print(f"You infuse the ground with Stormlight. The {enemy['name']} is [bold yellow]stuck[/bold yellow]!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

            # Lightweaver Logic
            elif player.order == "Lightweaver":
                if surge_choice == "1": # Illumination
                    if player.current_stormlight >= 8:
                        player.current_stormlight -= 8
                        player_dodging = True
                        console.print("You weave an illusion of yourself. The enemy is confused!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Soulcast
                    if player.current_stormlight >= 25:
                        player.current_stormlight -= 25
                        dmg = random.randint(30, 45)
                        enemy["hp"] -= dmg
                        console.print(f"You Soulcast the air into fire around the {enemy['name']}! [bold magenta]{dmg}[/bold magenta] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

            # Skybreaker Logic
            elif player.order == "Skybreaker":
                if surge_choice == "1": # Gravity Lashing
                    if player.current_stormlight >= 12:
                        player.current_stormlight -= 12
                        dmg = random.randint(18, 28)
                        enemy["hp"] -= dmg
                        console.print(f"You increase gravity around the {enemy['name']}! It crumples for [bold yellow]{dmg}[/bold yellow] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Division
                    if player.current_stormlight >= 18:
                        player.current_stormlight -= 18
                        dmg = random.randint(25, 40)
                        enemy["hp"] -= dmg
                        console.print(f"You touch the {enemy['name']} and it begins to split apart! [bold red]{dmg}[/bold red] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

            # Edgedancer Logic
            elif player.order == "Edgedancer":
                if surge_choice == "1": # Friction Slide
                    if player.current_stormlight >= 6:
                        player.current_stormlight -= 6
                        player_dodging = True
                        console.print("You become impossibly slippery! The enemy struggles to hit you!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Regrowth
                    if player.current_stormlight >= 15:
                        player.current_stormlight -= 15
                        heal_amount = 30
                        old_hp = player.current_hp
                        player.current_hp = min(player.max_hp, player.current_hp + heal_amount)
                        actual_heal = player.current_hp - old_hp
                        console.print(f"You channel Progression! Your wounds close rapidly. [bold green]+{actual_heal} HP[/bold green]")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

            # Elsecaller Logic
            elif player.order == "Elsecaller":
                if surge_choice == "1": # Soulcast
                    if player.current_stormlight >= 20:
                        player.current_stormlight -= 20
                        dmg = random.randint(22, 35)
                        enemy["hp"] -= dmg
                        console.print(f"You Soulcast the ground beneath the {enemy['name']} into lava! [bold orange1]{dmg}[/bold orange1] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")
                elif surge_choice == "2": # Elsecall
                    if player.current_stormlight >= 30:
                        player.current_stormlight -= 30
                        dmg = random.randint(35, 50)
                        enemy["hp"] -= dmg
                        console.print(f"You blink behind the {enemy['name']} and strike! [bold magenta]{dmg}[/bold magenta] damage!")
                        player_turn_done = True
                    else:
                        console.print("[dim]Not enough Stormlight![/dim]")

        elif action == "4":
            console.print("You attempt to flee!")
            # Flee has consequences
            if random.random() < 0.6:  # 60% success rate
                console.print("You escape back to the bridge!")
                # Lose some spheres in the panic
                sphere_loss = min(player.spheres, random.randint(1, 5))
                player.spheres -= sphere_loss
                if sphere_loss > 0:
                    console.print(f"[dim]You dropped {sphere_loss} spheres in your haste![/dim]")
                time.sleep(1)
                return False
            else:
                # Flee fails - enemy gets a free attack
                console.print("[bold red]The enemy catches you as you turn![/bold red]")
                dmg = random.randint(stats["damage"], stats["damage"]+5)
                actual_dmg = max(1, dmg - player.armor_bonus)
                player.current_hp -= actual_dmg
                console.print(f"You take [bold red]{actual_dmg}[/bold red] damage from behind!")
                time.sleep(1)
                if player.current_hp <= 0:
                    console.print("\n[bold red]YOU HAVE DIED.[/bold red]")
                    console.print("Your sphere fades...")
                    return False
                # Failed flee continues combat
                console.print("You're forced back into combat!")
                time.sleep(1)
            
        time.sleep(1)
        
        if not player_turn_done:
            continue # If they went back or failed a cast, don't let enemy attack
        
        # Enemy Turn
        if enemy["hp"] > 0:
            if enemy_stunned:
                console.print(f"The {enemy['name']} struggles against the Lashing but cannot move!")
                enemy_stunned = False # Stun lasts 1 turn
            else:
                # Special Ability Check (30% chance if available)
                special_ability = stats.get("special_ability")
                use_special = special_ability and random.random() < 0.3

                if use_special:
                    # Execute special ability
                    if special_ability == "piercing_shot":
                        dmg = random.randint(15, 20)
                        actual_dmg = max(1, dmg - (player.armor_bonus // 2))  # Piercing ignores half armor
                        player.current_hp -= actual_dmg
                        console.print(f"The {enemy['name']} fires a [bold orange1]piercing shot[/bold orange1]! [bold red]{actual_dmg}[/bold red] damage!")

                    elif special_ability == "multi_shot":
                        hits = random.randint(2, 3)
                        total_dmg = 0
                        for _ in range(hits):
                            dmg = random.randint(4, 7)
                            actual_dmg = max(1, dmg - player.armor_bonus)
                            total_dmg += actual_dmg
                        player.current_hp -= total_dmg
                        console.print(f"The {enemy['name']} fires [bold orange1]{hits} arrows[/bold orange1] at once! [bold red]{total_dmg}[/bold red] total damage!")

                    elif special_ability == "rage":
                        dmg = random.randint(20, 30)
                        actual_dmg = max(1, dmg - player.armor_bonus)
                        player.current_hp -= actual_dmg
                        console.print(f"The {enemy['name']} enters a [bold red]berserker rage[/bold red]! [bold red]{actual_dmg}[/bold red] damage!")

                    elif special_ability == "shard_strike":
                        dmg = random.randint(18, 25)
                        actual_dmg = dmg  # Shard weapons ignore armor
                        player.current_hp -= actual_dmg
                        console.print(f"The {enemy['name']} swings their [bold yellow]Shardblade[/bold yellow]! [bold red]{actual_dmg}[/bold red] damage ([dim]ignores armor[/dim])!")

                    elif special_ability == "drain_light":
                        light_drain = min(15, player.current_stormlight)
                        player.current_stormlight -= light_drain
                        console.print(f"The {enemy['name']} [bold magenta]drains[/bold magenta] {light_drain} Stormlight from you!")
                        # Also deal small damage
                        dmg = random.randint(8, 12)
                        actual_dmg = max(1, dmg - player.armor_bonus)
                        player.current_hp -= actual_dmg
                        console.print(f"And strikes for [bold red]{actual_dmg}[/bold red] damage!")

                    elif special_ability == "claw_swipe":
                        dmg = random.randint(25, 35)
                        actual_dmg = max(1, dmg - player.armor_bonus)
                        player.current_hp -= actual_dmg
                        console.print(f"The {enemy['name']} [bold red]swipes its massive claw[/bold red]! [bold red]{actual_dmg}[/bold red] damage!")

                else:
                    # Normal Attack
                    # Dodge Check
                    hit_chance = 50 if player_dodging else 100
                    if random.randint(1, 100) <= hit_chance:
                        dmg = random.randint(stats["damage"]-2, stats["damage"]+2)
                        # Apply armor reduction
                        actual_dmg = max(1, dmg - player.armor_bonus)
                        player.current_hp -= actual_dmg
                        if actual_dmg < dmg:
                            console.print(f"The {enemy['name']} hits you for [bold red]{actual_dmg}[/bold red] damage ([dim]{dmg-actual_dmg} blocked[/dim])!")
                        else:
                            console.print(f"The {enemy['name']} hits you for [bold red]{actual_dmg}[/bold red] damage!")
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