from rich.prompt import Prompt
from src.ui import console, print_header
import time
import random

def talk_to_spren(player):
    print_header()
    
    spren_name = "Syl" if player.order == "Windrunner" else "Pattern"
    spren_type = "Honorspren" if player.order == "Windrunner" else "Cryptic"
    
    console.print(f"\n[bold cyan]--- Communing with {spren_name} ---"[/bold cyan])
    console.print(f"[italic]Your {spren_type} manifests near you.[/italic]")
    
    # Dialogue options based on Level (Ideals)
    dialogues = []
    
    if player.level == 1:
        if player.order == "Windrunner":
            dialogues = [
                "The winds are restless today. They speak of a coming storm.",
                "Why do men kill? It is... confusing. You protect, but you also kill.",
                "Keep your word, Radiant. That is the most important thing."
            ]
        else: # Lightweaver
            dialogues = [
                "Mmm... delicious lies everywhere in this camp.",
                "The pattern of your soul is shifting. Fascinating.",
                "Do not trust what you see. Trust what you know."
            ]
    elif player.level >= 2:
         if player.order == "Windrunner":
            dialogues = [
                "You have spoken the Second Ideal. 'I will protect those who cannot protect themselves.' Do not forget it.",
                "I remember... I remember the Honor of old. It was heavy.",
                "The sky is yours, if you claim it."
            ]
         else:
            dialogues = [
                "You have admitted a Truth. That is good. The vibration of it is sweet.",
                "Shallan... no, that is another. You are you.",
                "Soulcasting is dangerous. To change a thing, you must understand it perfectly."
            ]
            
    # General advice
    dialogues.append("Do you need Stormlight? The gems in the market are dull, but they will serve.")
    
    chosen_text = random.choice(dialogues)
    console.print(f"\n[bold]{spren_name}:[/bold] \"{chosen_text}\"")
    
    # Interaction Menu
    console.print("\n1. Ask about the Radiants")
    console.print("2. Ask about the Enemy")
    console.print("3. Leave")
    
    choice = Prompt.ask("Say", choices=["1", "2", "3"], default="3")
    
    if choice == "1":
        console.print(f"\n[bold]{spren_name}:[/bold] \"We were once many. Now we are few. The Recreance... it broke us. But the bond can heal.\"")
    elif choice == "2":
        console.print(f"\n[bold]{spren_name}:[/bold] \"Odium. He reigns in the storms. He wants to break everything. We must not let him.\"")
    
    time.sleep(2)
