import os, subprocess
from engine.player import Player

def clear_screen():
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def load_fleet_from_file(player: Player, filename: str) -> bool:
    """Reads fleet config file, returns True if successfully deployed, False if not"""
    if not os.path.exists(filename):
        print(f"[Loader] Filename {filename} not found")
        return False
    
    print(f"[Loader] Reading config from {filename}...")
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) != 5:
                    print(f"[Loader] Syntax Error on line {line_num}: Expected 5 values, got {len(parts)}.")
                    return False
                
                name, x_str, y_str, len_str, ori_str = parts

                x = int(x_str.strip())
                y = int(y_str.strip())
                length = int(len_str.strip())
                vertical = ori_str.strip().lower() == "v"

                player.plot_ship(x, y, length, vertical)
                print(f"[Loader] Placed {name} (Size {length}) at ({x}, {y})")

        return True
    except ValueError as e:
        print(f"[Loader] Error loading ship config on line {line_num}: {e}")
        return False
    
def load_fleet_manifest(filename: str = "config/fleet_config.txt") -> list[tuple[str, int]]:
    """Reads the game configuration file to determine what ships are in play,
    allowing multiple quantities of each ship.
    
    Returns a flat list of (ship_name, length) tuples matching the quantities specified.
    """
    default_fleet = [("Carrier", 5), ("Battleship", 4), ("Destroyer", 3), ("Patrol Boat", 2)]

    if not os.path.exists(filename):
        print(f"[Loader] Config file {filename} does not exist. Using default fleet...")
        return default_fleet
    
    fleet_manifest = []
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) != 3:
                    print(f"[Loader] Syntax Error on line {line_num}: Expected 3 values, got {len(parts)}. Skipping")
                    continue
                
                name = parts[0].strip()
                length = int(parts[1].strip())
                quantity = int(parts[2].strip())

                if length <= 0 or quantity <= 0:
                    print(f"[Loader] Invalid ship properties on line {line_num}. Skipping")
                    continue

                for q in range(1, quantity + 1):
                    display_name = f"{name} {q}" if quantity > 1 else name
                    fleet_manifest.append((display_name, length))

        if not fleet_manifest:
            print(f"[Loader] Config file empty. Using default fleet.")
            return default_fleet

        return fleet_manifest
    
    except ValueError as e:
        print(f"[Loader] Error parsing ship config on line {line_num}: {e}. Using standard fleet")
        return default_fleet