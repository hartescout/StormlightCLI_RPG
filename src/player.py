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
        # Equipment System
        if order == "Windrunner":
            starting_weapon = "Basic Spear"
        elif order == "Skybreaker":
            starting_weapon = "Sunraiser Blade"
        elif order == "Edgedancer":
            starting_weapon = "Dual Daggers"
        elif order == "Elsecaller":
            starting_weapon = "Scholar's Staff"
        else:
            starting_weapon = "Dagger"

        self.inventory = []
        self.equipped_weapon = starting_weapon
        self.equipped_armor = "Bridge Crew Rags"
        self.damage_bonus = self._calculate_damage_bonus()
        self.armor_bonus = self._calculate_armor_bonus()
        
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

        # Get proper ordinal suffix
        def ordinal(n):
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return f"{n}{suffix}"

        # Stat Increases
        hp_gain = 20
        stormlight_gain = 10
        self.max_hp += hp_gain
        self.max_stormlight += stormlight_gain

        # Partial healing on level up (50% of new max)
        heal_amount = self.max_hp // 2
        light_gain = self.max_stormlight // 2
        self.current_hp = min(self.max_hp, self.current_hp + heal_amount)
        self.current_stormlight = min(self.max_stormlight, self.current_stormlight + light_gain)

        ideal_text = ordinal(self.level)
        console.print(f"\n[bold green]IDEAL SPOKEN! You have reached the {ideal_text} Ideal![/bold green]")
        console.print(f"Max HP +{hp_gain} (Now {self.max_hp})")
        console.print(f"Max Stormlight +{stormlight_gain} (Now {self.max_stormlight})")
        console.print(f"[cyan]Healed {heal_amount} HP and gained {light_gain} Stormlight![/cyan]")

    def status_panel(self):
        """Returns a formatted string or Renderable for the player status."""
        from rich.panel import Panel
        from rich.text import Text

        status_text = Text()
        status_text.append(f"Radiant: {self.name} ({self.order}) - Level {self.level}\n", style="bold white")
        status_text.append(f"HP: {self.current_hp}/{self.max_hp}\n", style="red")
        status_text.append(f"Stormlight: {self.current_stormlight}/{self.max_stormlight}\n", style="cyan")
        status_text.append(f"Spheres: {self.spheres} chips\n", style="yellow")
        status_text.append(f"Weapon: {self.equipped_weapon} (+{self.damage_bonus} dmg)\n", style="green")
        status_text.append(f"Armor: {self.equipped_armor} ({self.armor_bonus} def)\n", style="blue")
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

    def _calculate_damage_bonus(self):
        """Calculate damage bonus from equipped weapon."""
        weapons = {
            "Dagger": 0,
            "Basic Spear": 2,
            "Sunraiser Blade": 3,
            "Dual Daggers": 1,
            "Scholar's Staff": 1,
            "Shardblade": 15,
            "Sylspear": 8,
            "Lightweaver Blade": 6,
            "Justice's Edge": 7,
            "Healing Staff": 2,
            "Elsecaller's Wand": 5
        }
        return weapons.get(self.equipped_weapon, 0)

    def _calculate_armor_bonus(self):
        """Calculate damage reduction from equipped armor."""
        armors = {
            "Bridge Crew Rags": 0,
            "Leather Armor": 2,
            "Chain Mail": 4,
            "Plate Armor": 6,
            "Shardplate": 10
        }
        return armors.get(self.equipped_armor, 0)

    def equip_weapon(self, weapon_name):
        """Equip a weapon from inventory."""
        if weapon_name in self.inventory:
            # Put current weapon in inventory
            if self.equipped_weapon:
                self.inventory.append(self.equipped_weapon)
            # Equip new weapon
            self.equipped_weapon = weapon_name
            self.inventory.remove(weapon_name)
            self.damage_bonus = self._calculate_damage_bonus()
            return True
        return False

    def equip_armor(self, armor_name):
        """Equip armor from inventory."""
        if armor_name in self.inventory:
            # Put current armor in inventory
            if self.equipped_armor:
                self.inventory.append(self.equipped_armor)
            # Equip new armor
            self.equipped_armor = armor_name
            self.inventory.remove(armor_name)
            self.armor_bonus = self._calculate_armor_bonus()
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
            "equipped_weapon": self.equipped_weapon,
            "equipped_armor": self.equipped_armor,
            "damage_bonus": self.damage_bonus,
            "armor_bonus": self.armor_bonus,
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
        player.inventory = data.get("inventory", [])
        player.equipped_weapon = data.get("equipped_weapon", "Dagger")
        player.equipped_armor = data.get("equipped_armor", "Bridge Crew Rags")
        player.damage_bonus = data.get("damage_bonus", 0)
        player.armor_bonus = data.get("armor_bonus", 0)
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)
        player.xp_to_next_level = data.get("xp_to_next_level", 100)
        return player
