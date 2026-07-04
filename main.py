import argparse
import sys
from engine.modes import local_match, ai_match

import os
if os.name == "nt":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)  # Enable ANSI escape codes on Windows

def main():
    parser = argparse.ArgumentParser(description="Battleships Game")

    parser.add_argument(
        "action",
        choices=["play"],
        help="Action to perform. Currently only 'play' is supported.",
    )

    parser.add_argument(
        "modifiers",
        nargs="*",
        help="Modifiers for the action. Use 'ai' for AI opponent and 'fast' for quick setup.",
    )

    parser.add_argument(
        "--grid-size",
        type=int,
        default=10,
        help="Size of the grid (default: 10).",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    grid_size = args.grid_size

    modifiers = [m.lower().strip() for m in args.modifiers]

    is_ai = "ai" in modifiers
    is_fast = "fast" in modifiers

    for item in modifiers:
        if item not in ["ai", "fast"]:
            print(f"Unknown modifier: {item}")
            sys.exit(1)

    if is_ai:
        ai_match(grid_size, is_fast)
    else:
        local_match(grid_size, is_fast)

if __name__ == "__main__":
    main()