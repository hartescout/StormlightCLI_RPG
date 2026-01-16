from rich.prompt import Prompt, IntPrompt
from src.ui import console, print_header, print_error, print_success
import time

def weapon_shop(player):
    """Shop for purchasing weapons."""
    weapons = {
        "1": {"name": "Sylspear", "price": 80, "bonus": 8},
        "2": {"name": "Lightweaver Blade", "price": 70, "bonus": 6},
        "3": {"name": "Justice's Edge", "price": 75, "bonus": 7},
        "4": {"name": "Healing Staff", "price": 50, "bonus": 2},
        "5": {"name": "Elsecaller's Wand", "price": 65, "bonus": 5},
        "6": {"name": "Shardblade", "price": 200, "bonus": 15}
    }

    console.print("\n[bold]--- Weapon Merchant ---[/bold]")
    console.print(f"Current weapon: [green]{player.equipped_weapon}[/green] (+{player.damage_bonus} dmg)")
    console.print(f"You have [bold yellow]{player.spheres} spheres[/bold yellow].\n")

    for key, weapon in weapons.items():
        console.print(f"{key}. [bold]{weapon['name']}[/bold] ({weapon['price']} spheres) - +{weapon['bonus']} damage")
    console.print("7. Back")

    choice = Prompt.ask("Purchase weapon", choices=list(weapons.keys()) + ["7"])

    if choice == "7":
        return

    weapon = weapons[choice]
    if player.spheres >= weapon["price"]:
        player.spheres -= weapon["price"]
        player.inventory.append(weapon["name"])
        print_success(f"You purchased {weapon['name']}!")
        time.sleep(1)
    else:
        print_error("Not enough spheres.")
        time.sleep(1)

def armor_shop(player):
    """Shop for purchasing armor."""
    armors = {
        "1": {"name": "Leather Armor", "price": 30, "defense": 2},
        "2": {"name": "Chain Mail", "price": 60, "defense": 4},
        "3": {"name": "Plate Armor", "price": 100, "defense": 6},
        "4": {"name": "Shardplate", "price": 300, "defense": 10}
    }

    console.print("\n[bold]--- Armor Merchant ---[/bold]")
    console.print(f"Current armor: [blue]{player.equipped_armor}[/blue] ({player.armor_bonus} def)")
    console.print(f"You have [bold yellow]{player.spheres} spheres[/bold yellow].\n")

    for key, armor in armors.items():
        console.print(f"{key}. [bold]{armor['name']}[/bold] ({armor['price']} spheres) - {armor['defense']} defense")
    console.print("5. Back")

    choice = Prompt.ask("Purchase armor", choices=list(armors.keys()) + ["5"])

    if choice == "5":
        return

    armor = armors[choice]
    if player.spheres >= armor["price"]:
        player.spheres -= armor["price"]
        player.inventory.append(armor["name"])
        print_success(f"You purchased {armor['name']}!")
        time.sleep(1)
    else:
        print_error("Not enough spheres.")
        time.sleep(1)

def manage_inventory(player):
    """Manage equipment inventory."""
    while True:
        console.print("\n[bold]--- Your Inventory ---[/bold]")
        console.print(f"Equipped Weapon: [green]{player.equipped_weapon}[/green] (+{player.damage_bonus} dmg)")
        console.print(f"Equipped Armor: [blue]{player.equipped_armor}[/blue] ({player.armor_bonus} def)\n")

        if not player.inventory:
            console.print("[dim]Your inventory is empty.[/dim]")
            Prompt.ask("\nPress Enter to go back")
            return

        console.print("Items in inventory:")
        for idx, item in enumerate(player.inventory, 1):
            console.print(f"{idx}. {item}")

        console.print(f"{len(player.inventory) + 1}. Back")

        choices = [str(i) for i in range(1, len(player.inventory) + 2)]
        choice = Prompt.ask("Select item to equip", choices=choices)

        if choice == str(len(player.inventory) + 1):
            break

        item_idx = int(choice) - 1
        item = player.inventory[item_idx]

        # Determine if weapon or armor
        weapons = ["Sylspear", "Lightweaver Blade", "Justice's Edge", "Healing Staff",
                   "Elsecaller's Wand", "Shardblade", "Basic Spear", "Sunraiser Blade",
                   "Dual Daggers", "Scholar's Staff", "Dagger"]
        armors = ["Leather Armor", "Chain Mail", "Plate Armor", "Shardplate", "Bridge Crew Rags"]

        if item in weapons:
            player.equip_weapon(item)
            print_success(f"Equipped {item}!")
        elif item in armors:
            player.equip_armor(item)
            print_success(f"Equipped {item}!")
        else:
            print_error("Unknown item type.")

        time.sleep(1)

def visit_shop(player):
    while True:
        print_header()
        console.print(player.status_panel())
        console.print("\n[bold]--- The Apothecary ---[/bold]")
        console.print("[italic]An old ardent looks up from mixing herbs.[/italic]")
        console.print(f"You have [bold yellow]{player.spheres} spheres[/bold yellow].")
        
        console.print("\n[bold yellow]Consumables:[/bold yellow]")
        console.print("1. [bold green]Bandages[/bold green] (5 spheres) - Heals 20 HP")
        console.print("2. [bold cyan]Infused Chip[/bold cyan] (10 spheres) - Restores 10 Stormlight")

        console.print("\n[bold yellow]Equipment:[/bold yellow]")
        console.print("3. [bold]Weapons[/bold] - View weapon shop")
        console.print("4. [bold]Armor[/bold] - View armor shop")
        console.print("5. [bold]Inventory[/bold] - Manage your equipment")

        console.print("\n6. Leave")

        choice = IntPrompt.ask("What do you need?", choices=["1", "2", "3", "4", "5", "6"])
        
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
            weapon_shop(player)

        elif choice == 4:
            armor_shop(player)

        elif choice == 5:
            manage_inventory(player)

        elif choice == 6:
            break
            
        time.sleep(1)
