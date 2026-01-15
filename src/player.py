import json
from src.ui import console

class Player:
    def __init__(self, name, order, stats):
        self.name = name
        self.order = order
        self.max_hp = stats["base_hp"]
        self.current_hp = self.max_hp
        self.max_stormlight = stats["base_stormlight"]
        self.current_stormlight = 0  # Start with no stormlight
        self.surges = stats["surges"]
        self.spheres = 5  # Starting currency/battery
        self.inventory = ["Basic Spear" if order == "Windrunner" else "Dagger"]
        self.damage_bonus = 0
        
        # Leveling System
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

    def gain_xp(self, amount):
        from src.ui import console
        self.xp += amount
        console.print(f"[bold yellow]+{amount} XP[/bold yellow]")
        
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        from src.ui import console
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Stat Increases
        hp_gain = 20
        stormlight_gain = 10
        self.max_hp += hp_gain
        self.current_hp = self.max_hp
        self.max_stormlight += stormlight_gain
        self.current_stormlight = self.max_stormlight # Full heal on level up
        
        console.print(f"\n[bold green]IDEAL SPOKEN! You have reached the {self.level}nd Ideal![/bold green]")
        console.print(f"Max HP +{hp_gain} (Now {self.max_hp})")
        console.print(f"Max Stormlight +{stormlight_gain} (Now {self.max_stormlight})")

    def status_panel(self):
        """Returns a formatted string or Renderable for the player status."""
        from rich.panel import Panel
        from rich.text import Text
        
        status_text = Text()
        status_text.append(f"Radiant: {self.name} ({self.order}) - Level {self.level}\n", style="bold white")
        status_text.append(f"HP: {self.current_hp}/{self.max_hp}\n", style="red")
        status_text.append(f"Stormlight: {self.current_stormlight}/{self.max_stormlight}\n", style="cyan")
        status_text.append(f"Spheres: {self.spheres} chips\n", style="yellow")
        status_text.append(f"XP: {self.xp}/{self.xp_to_next_level}", style="dim white")
        
        return Panel(status_text, title="Status", border_style="blue")

    def breathe_stormlight(self, amount):
        needed = self.max_stormlight - self.current_stormlight
        intake = min(amount, needed)
        self.current_stormlight += intake
        return intake

    def heal(self):
        if self.current_stormlight >= 5 and self.current_hp < self.max_hp:
            heal_amount = 10
            self.current_stormlight -= 5
            self.current_hp = min(self.max_hp, self.current_hp + heal_amount)
            return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "order": self.order,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "max_stormlight": self.max_stormlight,
            "current_stormlight": self.current_stormlight,
            "surges": self.surges,
            "spheres": self.spheres,
            "inventory": self.inventory,
            "damage_bonus": self.damage_bonus,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level
        }

    @classmethod
    def from_dict(cls, data):
        # Create a dummy stats dict to satisfy __init__
        stats = {
            "base_hp": data["max_hp"],
            "base_stormlight": data["max_stormlight"],
            "surges": data["surges"]
        }
        player = cls(data["name"], data["order"], stats)
        player.current_hp = data["current_hp"]
        player.current_stormlight = data["current_stormlight"]
        player.spheres = data["spheres"]
        player.inventory = data["inventory"]
        player.damage_bonus = data.get("damage_bonus", 0)
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)
        player.xp_to_next_level = data.get("xp_to_next_level", 100)
        return player
