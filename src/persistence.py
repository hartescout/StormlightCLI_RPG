import json
import os
from src.ui import console, print_success, print_error
from src.player import Player

SAVE_FILE = "savegame.json"

def save_game(player):
    try:
        data = player.to_dict()
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print_success("Game saved successfully.")
    except Exception as e:
        print_error(f"Failed to save game: {e}")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print_error("No save file found.")
        return None

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        player = Player.from_dict(data)
        print_success(f"Welcome back, {player.name}.")
        return player
    except json.JSONDecodeError:
        print_error("Save file is corrupted or invalid.")
        return None
    except KeyError as e:
        print_error(f"Save file is missing required data: {e}")
        return None
    except Exception as e:
        print_error(f"Failed to load save file: {e}")
        return None
