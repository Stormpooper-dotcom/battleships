from engine.player import Player
from engine.utils import clear_screen

def get_ship_placement(player: Player, ship_name: str, length: int) -> None:
    while True:
        print(player)
        print(f"\nPLAYER {player.id}: Deploying {ship_name} (Length: {length})")

        coords_input = input("Enter start pos as 'x y': ").strip()
        try:
            x_str, y_str = coords_input.split()
            x, y = int(x_str), int(y_str)
        except ValueError:
            print("Invalid format!")
            input("Press Enter...")
            clear_screen()
            continue

        dir_input = input("Enter orientation - 'v' for Vertical, 'h' for Horizontal: ").strip().lower()
        if dir_input not in ['v', 'h']:
            print("Invalid orientation! Use 'v' or 'h'.")
            input("Press Enter...")
            clear_screen()
            continue
        
        vertical = (dir_input == 'v')

        try:
            player.plot_ship(x, y, length, vertical)
            input(f"{ship_name} deployed successfully!")
            clear_screen()
            break
        except ValueError as e:
            print(f"{e}")
            input("Press Enter...")
            clear_screen()
            continue