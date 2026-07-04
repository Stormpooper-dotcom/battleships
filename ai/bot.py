import random
from engine.player import Player

class BattleshipAI:
    def __init__(self, size: int, id: int) -> None:
        self.player_profile = Player(size, size, id)
        self.size = size
        self.fired_coordinates = set()
        self.target_queue = []

    def auto_deploy_fleet(self, fleet_manifest: list[tuple[str, int]]) -> None:
        print(f"[AI] Received a manifest of {len(fleet_manifest)} ships to place.")
        for name, length in fleet_manifest:
            placed = False
            attempts = 0
            
            while not placed:
                attempts += 1
                if attempts > 1000:
                    print(f"[AI] Error: Could not find space for '{name}' after 1000 tries. Skipping.")
                    break
                    
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                vertical = random.choice([True, False])
                
                try:
                    # Call the core engine grid plotter
                    self.player_profile.plot_ship(x, y, length, vertical)
                    placed = True
                except ValueError as e:
                    # If it's a legitimate overlap/out-of-bounds, continue hunting
                    if "bounds" in str(e) or "Overlap" in str(e):
                        continue
                    # If it's a different runtime error (like data type mismatch), log it!
                    print(f"[AI] Internal Error plotting '{name}': {e}")
                    break
        print(f"[AI] Fleet deployment complete. {len(self.player_profile.ships)} ships placed successfully.")
    
    def calculate_next_move(self) -> tuple[int, int]:
        # Target Phase
        while self.target_queue:
            tx, ty = self.target_queue.pop(0)
            if (tx, ty) not in self.fired_coordinates:
                self.fired_coordinates.add((tx, ty))
                return tx, ty
            
        # Hunt Phase
        while True:
            rx = random.randint(0, self.size - 1)
            ry = random.randint(0, self.size - 1)
            if (rx, ry) not in self.fired_coordinates:
                self.fired_coordinates.add((rx, ry))
                return rx, ry
            
    def process_shot_result(self, x: int, y: int, result_string: str) -> None:
        if "hit" in result_string.lower():
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if (nx, ny) not in self.fired_coordinates:
                        self.target_queue.append((nx, ny))