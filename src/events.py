import random
import time
from rich.prompt import Prompt
from src.ui import console, print_header

def event_arrow_volley(player):
    console.print("\n[bold red]WARNING![/bold red] A horn blows in the distance.")
    console.print("Parshendi archers on the next plateau loose a volley of arrows!")
    console.print("The sky darkens with falling death.")
    
    console.print("\n1. [bold]Raise Shield[/bold] (Hope for the best)")
    console.print("2. [bold cyan]Use Stormlight[/bold cyan] (Deflect/Dodge - Costs 10 Light)")
    
    choice = Prompt.ask("Action", choices=["1", "2"])
    
    if choice == "1":
        # Random chance of hit
        if random.random() < 0.6:
            dmg = random.randint(10, 25)
            player.current_hp -= dmg
            console.print(f"An arrow punches through your wooden shield! You take [bold red]{dmg}[/bold red] damage.")
        else:
            console.print("Arrows thud harmlessly into the wood around you. You are safe.")
            
    elif choice == "2":
        if player.current_stormlight >= 10:
            player.current_stormlight -= 10
            if player.order == "Windrunner":
                console.print("You Lash the arrows upward! They veer away harmlessly.")
            elif player.order == "Lightweaver":
                console.print("You weave an illusion of the bridge crew elsewhere. The arrows miss completely.")
            elif player.order == "Skybreaker":
                console.print("You use Gravitation to deflect the arrows sideways!")
            elif player.order == "Edgedancer":
                console.print("You slide impossibly fast, arrows missing by inches!")
            elif player.order == "Elsecaller":
                console.print("You briefly shift to Shadesmar, letting the arrows pass through you!")
            else:
                console.print("You infuse your skin, letting the arrows glance off.")
        else:
            console.print("You reach for the Light, but it is gone! You raise your shield in panic.")
            dmg = random.randint(15, 30) # More damage for failing
            player.current_hp -= dmg
            console.print(f"You take [bold red]{dmg}[/bold red] damage.")

def event_chasm_jump(player):
    console.print("\nThe bridge is down, but the mechanism is jammed!")
    console.print("You need to cross the chasm to secure the landing.")
    console.print("Below you, the darkness is absolute.")
    
    console.print("\n1. [bold]Jump manually[/bold] (Athletics check)")
    console.print("2. [bold cyan]Infuse and Leap[/bold cyan] (Costs 5 Light)")
    
    choice = Prompt.ask("Action", choices=["1", "2"])
    
    if choice == "1":
        if random.random() < 0.7:
             console.print("You scramble across the gap, fingers digging into the rock. Safe.")
        else:
             dmg = random.randint(5, 15)
             player.current_hp -= dmg
             console.print(f"You slip! You catch yourself, but scrape your arm badly. [bold red]-{dmg} HP[/bold red].")
             
    elif choice == "2":
        if player.current_stormlight >= 5:
            player.current_stormlight -= 5
            console.print("Stormlight makes you light as a feather. You bound across the chasm easily.")
            # Small XP reward for using powers coolly?
            player.gain_xp(10)
        else:
             console.print("Not enough Light! You jump anyway...")
             dmg = random.randint(5, 15)
             player.current_hp -= dmg
             console.print(f"You stumble and take [bold red]{dmg}[/bold red] damage.")

def event_wounded_bridgeman(player):
    console.print("\nDuring a lull in the charge, you spot a fellow bridgeman on the ground.")
    console.print("He's bleeding out from a spear wound.")
    
    console.print("\n1. [bold]Leave him[/bold] (Save resources)")
    console.print("2. [bold cyan]Heal him[/bold cyan] (Costs 15 Light - High Reward)")
    
    choice = Prompt.ask("Action", choices=["1", "2"])
    
    if choice == "1":
        console.print("You grit your teeth and keep moving. He is lost to the Void.")
        
    elif choice == "2":
        if player.current_stormlight >= 15:
            player.current_stormlight -= 15
            console.print("You press your hands to his wound. The skin knits together. He gasps in wonder.")
            console.print("\"Thank you... thank you!\"")
            console.print("He hands you a pouch he found.")
            spheres = random.randint(10, 20)
            player.spheres += spheres
            console.print(f"[bold yellow]+{spheres} Spheres[/bold yellow]")
            player.gain_xp(30) # Good karma XP
        else:
            console.print("You try to help, but you have no Light to give. He passes away in your arms.")
            # Maybe a morale penalty? For now just text.

def event_falling_boulder(player):
    console.print("\nRumbling echoes from the chasm walls!")
    console.print("A massive boulder breaks loose and tumbles toward the bridge crew!")

    console.print("\n1. [bold]Dive out of the way[/bold] (Risk injury)")
    console.print("2. [bold cyan]Use Stormlight[/bold cyan] (Push it away - Costs 12 Light)")

    choice = Prompt.ask("Action", choices=["1", "2"])

    if choice == "1":
        if random.random() < 0.5:
            console.print("You roll clear just in time!")
        else:
            dmg = random.randint(12, 20)
            player.current_hp -= dmg
            console.print(f"The boulder clips your leg! [bold red]-{dmg} HP[/bold red].")

    elif choice == "2":
        if player.current_stormlight >= 12:
            player.current_stormlight -= 12
            if player.order == "Windrunner":
                console.print("You Lash the boulder upward! It sails over your heads.")
            elif player.order == "Skybreaker":
                console.print("You reverse gravity on the boulder! It floats away.")
            elif player.order == "Elsecaller":
                console.print("You Soulcast the boulder into smoke!")
            else:
                console.print("You push the boulder aside with raw Stormlight!")
            player.gain_xp(15)
        else:
            console.print("Not enough Light! You scramble desperately...")
            dmg = random.randint(15, 25)
            player.current_hp -= dmg
            console.print(f"The boulder catches you! [bold red]-{dmg} HP[/bold red].")

def event_chasm_treasure(player):
    console.print("\nYou spot something glinting in a crack in the chasm wall.")
    console.print("It looks like a pouch of spheres, but reaching it is dangerous.")

    console.print("\n1. [bold]Ignore it[/bold] (Safe)")
    console.print("2. [bold]Reach for it[/bold] (Risky)")

    choice = Prompt.ask("Action", choices=["1", "2"])

    if choice == "1":
        console.print("You keep moving. Survival is more important than spheres.")

    elif choice == "2":
        if random.random() < 0.6:
            spheres = random.randint(8, 15)
            player.spheres += spheres
            console.print(f"You snag the pouch! [bold yellow]+{spheres} Spheres[/bold yellow]")
        else:
            dmg = random.randint(5, 10)
            player.current_hp -= dmg
            console.print(f"Your hand slips on the wet rock! [bold red]-{dmg} HP[/bold red].")

def event_parshendi_drummer(player):
    console.print("\nYou hear rhythmic drumming from ahead.")
    console.print("A Parshendi war drummer is rallying their troops!")

    console.print("\n1. [bold]Ignore and advance[/bold] (Face tougher enemies)")
    console.print("2. [bold cyan]Silence the drummer[/bold cyan] (Use Light - Costs 8)")

    choice = Prompt.ask("Action", choices=["1", "2"])

    if choice == "1":
        console.print("The drums grow louder. The enemy will be strengthened...")
        # This will be reflected in combat difficulty (we can add a flag)

    elif choice == "2":
        if player.current_stormlight >= 8:
            player.current_stormlight -= 8
            console.print("You silence the drummer with a surge-enhanced throw!")
            spheres = random.randint(5, 10)
            player.spheres += spheres
            player.gain_xp(20)
            console.print(f"[bold yellow]+{spheres} Spheres[/bold yellow]")
        else:
            console.print("Not enough Light! The drummer escapes.")

def event_bridge_collapse(player):
    console.print("\n[bold red]CRACK![/bold red] The bridge begins to splinter under the weight!")
    console.print("You need to move fast or fall into the chasm!")

    console.print("\n1. [bold]Sprint across[/bold] (Athletics check)")
    console.print("2. [bold cyan]Lighten yourself[/bold cyan] (Costs 10 Light)")

    choice = Prompt.ask("Action", choices=["1", "2"])

    if choice == "1":
        if random.random() < 0.65:
            console.print("You sprint across just as the bridge collapses behind you!")
        else:
            dmg = random.randint(10, 18)
            player.current_hp -= dmg
            console.print(f"You fall but catch the edge! You pull yourself up. [bold red]-{dmg} HP[/bold red].")

    elif choice == "2":
        if player.current_stormlight >= 10:
            player.current_stormlight -= 10
            console.print("Stormlight makes you weightless! You practically float across!")
        else:
            console.print("Not enough Light! You stumble...")
            dmg = random.randint(10, 18)
            player.current_hp -= dmg
            console.print(f"[bold red]-{dmg} HP[/bold red].")

def start_bridge_run(player):
    print_header()
    console.print("[bold yellow]--- BRIDGE RUN INITIATED ---[/bold yellow]")
    console.print("The horn sounds. The bridge crews lift. You run toward the next plateau.")
    time.sleep(2)

    # Expanded Event Pool
    event_pool = [
        event_arrow_volley,
        event_chasm_jump,
        event_wounded_bridgeman,
        event_falling_boulder,
        event_chasm_treasure,
        event_parshendi_drummer,
        event_bridge_collapse
    ]
    chosen_event = random.choice(event_pool)
    chosen_event(player)

    if player.current_hp <= 0:
        return False # Died in event

    time.sleep(1)
    console.print("\n[italic]You reach the other side. The Parshendi are waiting.[/italic]")
    time.sleep(1)

    # Proceed to Combat
    from src.combat import combat_encounter
    return combat_encounter(player)
