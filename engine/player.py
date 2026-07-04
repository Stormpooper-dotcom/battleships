from __future__ import annotations

class Colours:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    BLUE = "\033[34m"
    GREEN = "\033[32m"
    ORANGE = "\033[33m"
    RED = "\033[31m"
    
class Player:
    def __init__(self, x: int, y: int, id: int) -> None:
        self.hit_board = [[0 for _ in range(x)] for _ in range(y)]
        self.ship_board = [[0 for _ in range(x)] for _ in range(y)]
        self.id = id

        self.ships: list[dict] = []

    def plot_ship(self, x: int, y: int, length: int, vertical: bool) -> None:
        if vertical:
            if y + length > len(self.ship_board):
                raise ValueError("Cannot place ship: Ship goes out of vertical bounds")
            
            for i in range(length):
                if self.ship_board[y + i][x] == 1:
                    raise ValueError("Cannot place ship: Overlaps with existing ship")

        else:
            if x + length > len(self.ship_board[0]):
                raise ValueError("Cannot place ship: Ship goes out of horizontal bounds")
            
            for i in range(length):
                if self.ship_board[y][x + i] == 1:
                    raise ValueError("Cannot place ship: Overlaps with existing ship")

        current_ship_coords = []
        for i in range(length):
            nx, ny = (x, y + i) if vertical else (x + i, y)
            self.ship_board[ny][nx] = 1
            current_ship_coords.append((nx, ny))
        
        self.ships.append({
            "remaining": current_ship_coords,
            "original_coords": list(current_ship_coords)
            })
    
    def make_move(self, x: int, y: int, other_player: Player) -> str:
        if not self.move_valid(x, y):
            return "Invalid Move"
        
        result, sunk_coords = other_player.register_hit(x, y)

        if result == "hit":
            self.hit_board[y][x] = 1
        elif result == "sunk":
            self.hit_board[y][x] = 2
            self._mark_ship_sunk(sunk_coords)
        else:
            self.hit_board[y][x] = -1

        return result

    def _mark_ship_sunk(self, sunk_coords: list[tuple[int, int]]):
        for sx, sy in sunk_coords:
            self.hit_board[sy][sx] = 2

    def register_hit(self, x: int, y: int) -> tuple[str, list[tuple[int, int]]]:
        if self.ship_board[y][x] != 1:
            self.ship_board[y][x] = -1
            return "miss", []
        
        for ship in self.ships:
            if (x, y) in ship["remaining"]:
                ship["remaining"].remove((x, y))

                if len(ship["remaining"]) == 0:
                    self.ships.remove(ship)
                    for sx, sy in ship["original_coords"]:
                        self.ship_board[sy][sx] = 2
                    return "sunk", ship["original_coords"]
                
                self.ship_board[y][x] = -1
                return "hit", []
        
        return "miss", []
    
    def move_valid(self, x: int, y: int) -> bool:
        if not (0 <= x < len(self.hit_board[0]) and 0 <= y < len(self.hit_board)):
            return False
        return self.hit_board[y][x] == 0
    
    def has_lost(self) -> bool:
        for row in self.ship_board:
            if 1 in row:
                return False
        return True
    
    def __str__(self):
        # hit_board: 0=nothing, 1=hit (X), 2=sunk (#), -1=miss(M)
        # ship_board: 0=nothing, 1=ship(S), 2=sunk (#), -1=opponent_guess (G)
        symbols = {0: ".", 1: "X", -1: "M", 2: "#", "ship": "S", "guess": "G"}

        lines = []
        lines.append(f"{Colours.BOLD}=== Player {self.id} ==={Colours.RESET}")

        height = len(self.ship_board)
        width = len(self.ship_board[0])

        total_board_width = width * 2
        title_padding = max(2, total_board_width - 9)
        board_title_row = f"   SHIP BOARD{" " * title_padding}   HIT BOARD"
        lines.append(f"{Colours.BOLD}{board_title_row}{Colours.RESET}")

        tens_chars = ["  "]
        for x in range(width):
            tens_chars.append(str(x // 10) if x >= 10 else " ")
        tens_str = " ".join(tens_chars)
        lines.append(f"{tens_str}    {tens_str}")

        units_chars = [str(x % 10) for x in range(width)]
        units_str = " ".join(units_chars)
        lines.append(f"   {units_str}       {units_str}")

        for y in range(height): 
            # Build ship board row
            ship_row_chars = []
            for x in range(width):
                val = self.ship_board[y][x]
                if val == 1:
                    ship_row_chars.append(f"{Colours.GREEN}{symbols['ship']}{Colours.RESET}")
                elif val == 2:
                    ship_row_chars.append(f"{Colours.RED}{symbols[2]}{Colours.RESET}")
                elif val == -1:
                    ship_row_chars.append(f"{Colours.ORANGE}{symbols['guess']}{Colours.RESET}")
                else:
                    ship_row_chars.append(f"{Colours.BLUE}{symbols[0]}{Colours.RESET}")
            ship_row_str = " ".join(ship_row_chars)

            # Build hit board row
            hit_row_chars = []
            for x in range(width):
                val = self.hit_board[y][x]
                if val == 1:
                    hit_row_chars.append(f"{Colours.ORANGE}{symbols[1]}{Colours.RESET}")
                elif val == 2:
                    hit_row_chars.append(f"{Colours.RED}{symbols[2]}{Colours.RESET}")
                elif val == -1:
                    hit_row_chars.append(f"{Colours.GREEN}{symbols[-1]}{Colours.RESET}")
                else:
                    hit_row_chars.append(f"{Colours.BLUE}{symbols[0]}{Colours.RESET}")
            hit_row_str = " ".join(hit_row_chars)

            # {:2d} ensures both 1-digit and 2-digit numbers take exactly 2 spaces
            lines.append(f"{y:2d} {ship_row_str}    {y:2d} {hit_row_str}")

        return "\n".join(lines)