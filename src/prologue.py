from src.ui import console
import time

def play_prologue(player):
    console.print("\n" * 2)
    console.print("[bold]PROLOGUE: THE BROKEN[/bold]", justify="center")
    console.print("=" * 30, justify="center")
    time.sleep(2)

    if player.order == "Windrunner":
        console.print("\n[italic]The wood of the bridge digs into your shoulder. The weight is unbearable.[/italic]")
        time.sleep(2)
        console.print("Around you, men cough and stumble. You are Bridge Four. The expendables.")
        console.print("Sadeas rides past on a white stallion, armor gleaming, not sparing you a glance.")
        time.sleep(3)
        console.print("\n\"Why do you care?\" a small voice asks.")
        console.print("A ribbon of light dances in the air before you. A windspren? No... something else.")
        time.sleep(2)
        console.print("\n[bold cyan]\"I protect,\"[/bold cyan] you whisper, though you don't know why.")
        console.print("The light pulses. [bold]Then survive, Radiant. The storm comes.[/bold]")

    elif player.order == "Lightweaver":
        console.print("\n[italic]The warcamp is a chaotic mess of noise and color. You sit in the corner of the tent, sketching.[/italic]")
        time.sleep(2)
        console.print("Your family thinks you are here to ward. You are here to steal.")
        console.print("But the shadows on the page are wrong. They... move.")
        time.sleep(3)
        console.print("\n\"Mmm... a powerful lie,\" a buzzing vibration sounds from your skirt.")
        console.print("A pattern on the fabric twists, forming a geometric impossibility.")
        time.sleep(2)
        console.print("\n[bold magenta]\"It is not a lie,\"[/bold magenta] you think. [bold magenta]It is art.[/bold magenta]")
        console.print("[bold]Everything is a lie until it is true,\"[/bold] the pattern hums. [bold]Shall we find the truth?[/bold]")

    time.sleep(4)
    console.print("\n" + "=" * 30, justify="center")
    console.print("[dim]Press Enter to begin...[/dim]", justify="center")
    input()
