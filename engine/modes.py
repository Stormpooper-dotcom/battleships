from engine.player import Player
from engine.utils import clear_screen, load_fleet_from_file, load_fleet_manifest
from engine.controller import HumanController, AIController
from ai.bot import BattleshipAI
import os

def run_match(size: int, c1: HumanController, c2: HumanController | AIController):
    """The SINGLE universal game loop runner. It executes any combination of Human or AI opponents dynamically.
    """
    input("\nFleets deployed. Press Enter to begin the match...")
    
    active, opponent = c1, c2

    while True:
        clear_screen()
        print(f"\nPLAYER {active.player.id}'S TURN")
        
        # If it's a human, prompt them to avoid screen peeking
        if isinstance(active, HumanController):
            input("Press Enter to reveal your command boards...")
            clear_screen()
            print(active.player)

        # Get strategic move coordinates from the active controller abstraction
        move = active.get_move()
        
        if move == "q":
            print("Game terminated.")
            break
        elif move == "invalid_format":
            input("Formatting error. Input 2 numbers separated by a space. Press Enter...")
            continue

        if isinstance(move, tuple):
            x, y = move

            # Validate coordinate parameters against the board grid layout matrix
            if not active.player.move_valid(x, y):
                # AI calculations are natively clean, so this is mostly a safeguard for Humans
                if isinstance(active, HumanController):
                    input("Invalid target! Coordinates out of bounds or already targeted. Press Enter...")
                continue

            # Execute move and log result
            result_report = active.player.make_move(x, y, opponent.player)
            active.register_result(x, y, result_report)

            # Visual update state block
            clear_screen()
            if isinstance(active, HumanController):
                print(active.player)
            print(f"\nREPORT: Player {active.player.id} fired at ({x}, {y}) -> {result_report}")
        
        else:
            continue # Fallback just in case an unhandles string gets through, though it should never happen.

        if opponent.player.has_lost():
            print(f"\nMATCH OVER: PLAYER {active.player.id} WINS THE GAME!")
            break

        input("\nTurn complete. Press Enter to clear screen and swap controls...")
        active, opponent = opponent, active

def parse_ships_from_file(filename: str) -> list[tuple[str, int]]:
    """Helper to read names and lengths from a placement file for the AI.
    
    Correctly extracts the ship name (index 0) and length (index 3)
    from a 5-column comma-separated placement line (e.g., Carrier,1,1,5,h).
    """
    manifest = []
    if not os.path.exists(filename):
        # Fallback if file is completely missing
        return [("Carrier", 5), ("Battleship", 4), ("Destroyer", 3), ("Patrol Boat", 2)]
        
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                parts = line.split(",")
                if len(parts) != 5:
                    print(f"[AI] Parse Warning: Line {line_num} in '{filename}' does not have 5 parameters. Skipping.")
                    continue
                
                # FIX: Index 0 is the Name, Index 3 is the Length
                name = parts[0].strip()
                try:
                    length = int(parts[3].strip())
                    print(f"[AI] Parsed ship: {name} with length {length} from line {line_num}.")
                except ValueError:
                    print(f"[AI] Parse Warning: Line {line_num} has an invalid integer for length. Skipping.")
                    continue
                
                manifest.append((name, length))
                
        # If the file was completely empty or failed to gather ships, return fallback defaults
        if not manifest:
            return [("Carrier", 5), ("Battleship", 4), ("Destroyer", 3), ("Patrol Boat", 2)]
            
        return manifest
        
    except Exception as e:
        print(f"[AI] Error reading manifest: {e}. Defaulting fleet setup configuration rules.")
        return [("Carrier", 5), ("Battleship", 4), ("Destroyer", 3), ("Patrol Boat", 2)]
    
def local_match(size: int, fast: bool):
    """Handles both manual setup and file loading for Local 2-Player modes."""
    p1 = Player(size, size, 1)
    p2 = Player(size, size, 2)
    c1 = HumanController(p1)
    c2 = HumanController(p2)

    if fast:
        if load_fleet_from_file(p1, "config/player1_fleet.txt") and load_fleet_from_file(p2, "config/player2_fleet.txt"):
            print("[Setup] Both fleets successfully deployed from configuration files.")
            run_match(size, c1, c2)
        else:
            print("[Setup] File deployment failed. Check target paths or files structure layout.")
    else:
        fleet = load_fleet_manifest()
        clear_screen()
        print("=== PLAYER 1 PREPARATION ===")
        c1.deploy_fleet(fleet)
        clear_screen()
        print("=== PLAYER 2 PREPARATION ===")
        c2.deploy_fleet(fleet)
        run_match(size, c1, c2)

def ai_match(size: int, fast: bool):
    """Handles both manual setup and file loading for Solo vs AI modes."""
    p1 = Player(size, size, 1)
    c1 = HumanController(p1)
    ai_backend = BattleshipAI(size, id=2)
    c2 = AIController(p1, ai_backend)  # p1 is just a placeholder here; the AI uses its own player profile internally.

    if fast:
        # Load human profile from file
        if load_fleet_from_file(p1, "config/player1_fleet.txt"):
            # REQUIREMENT CHECK: AI loads configuration explicitly via player1_fleet.txt structure
            ai_fleet_rules = parse_ships_from_file("config/player1_fleet.txt")
            c2.deploy_fleet(ai_fleet_rules)
            print("[Setup] Human fleet loaded from file. AI initialized matching identical sizes.")
            run_match(size, c1, c2)
        else:
            print("[Setup] Human file deployment failed. Cannot initialize AI opponent profile.")
    else:
        # Standard configuration behavior from global manifest
        fleet = load_fleet_manifest()
        clear_screen()
        print("=== HUMAN FLEET DEPLOYMENT ===")
        c1.deploy_fleet(fleet)
        c2.deploy_fleet(fleet)
        run_match(size, c1, c2)