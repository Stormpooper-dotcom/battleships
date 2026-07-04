# battleships

A modular, terminal-based implementation of the classic Battleship board game written in Python. This project follows a professional **Model-View-Controller (MVC)** design pattern, using polymorphism to cleanly handle human players, algorithmic computer AI, and dynamic configuration loading via a unified command-line interface (CLI).

---

## Features
*   **Modular Architecture**: Isolated business logic (Engine) completely separate from decision mechanics (Controllers) and visual terminals (UI).
*   **Smart Hunt-and-Target AI**: A custom state-machine bot that hunts randomly until it scores a hit, immediately transitioning to tracking down neighboring coordinate fields.
*   **Fully Configurable Fleets**: Adjust match rules (ship types, quantities, sizes) instantly by editing local text assets.
*   **Fast Configuration Injection**: Skip the deployment phase by loading preset layouts straight from human and opponent player profile files.
*   **Dynamic Visual Sinking**: Damaged components are uniquely tracked; the moment an entire ship goes down, its connected segments instantly transform into `###` on both screens.
*   **Vibrant ANSI Visual Themes**: Full color-coded grid layouts (Blue water, Green ships/misses, Orange hits/guesses, Red explosions) for instant board scanning.

---

## Repository Layout
```text
battleship_game/
│
├── config/                  # Game rule specifications and coordinates matrices
│   ├── fleet_config.txt     # Global manifests (Type, Size, Quantities)
│   ├── player1_fleet.txt    # Fast-load layout profiles for Player 1
│   └── player2_fleet.txt    # Fast-load layout profiles for Player 2
│
├── ai/                      # Computer tactical engines
│   └── bot.py               # Hunt-and-Target state machine algorithms
│
├── engine/                  # Core mechanics and rule validation blocks
│   ├── player.py            # The Model: 2D grids, scores, and ship vectors
│   ├── controller.py        # The Controller: Interface remapping (Human/AI)
│   ├── utils.py             # File parsers and environment terminal utilities
│   ├── ui.py                # The View: Command line text menus
│   └── modes.py             # Match orchestrators and combat handlers
│
├── main.py                  # CLI argument routers and entry point
└── README.md                # Project documentation documentation
```

---

## Configuration Syntax
### 1. Global Ship Config (`config/fleet_config.txt`)
Define what ships are valid for standard manual placement games.
*   *Syntax*: `ShipName, Length, Quantity`
```text
Carrier,5,1
Battleship,4,1
Destroyer,3,2
Patrol Boat,2,1
```

### 2. Layout Fast-Loading (`config/player1_fleet.txt`)
Skip placement loops by writing preset positions. 
*   *Syntax*: `ShipName, StartX, StartY, Length, Orientation(v/h)`
```text
Carrier,1,1,5,h
Battleship,4,3,4,v
```
*(Note: In **AI Fast** mode, the AI automatically reads `player1_fleet.txt` to mirror the exact fleet size configuration loaded by the human).*

---

## Execution and Command Reference
Run the application from your root terminal using standard argument syntax. 

```bash
# 1. Local Pass-and-Play (2 Players, manual layout loops)
python main.py play

# 2. Solo vs Computer AI (Manual placement for you, AI random-scatters)
python main.py play ai

# 3. Fast Pass-and-Play (Loads p1_fleet.txt and p2_fleet.txt instantly)
python main.py play fast

# 4. Solo vs AI Fast (Loads your setup from file; AI clones matching sizes)
python main.py play ai fast

# Adjust Grid Dimensions (Optional global argument override)
python main.py play ai --grid-size 12
```

---

## Interface Controls and Mechanics
*   **Attack Entry**: Enter your coordinates as a space-separated pair (`x y`). For example: `4 2` targets Column 4, Row 2.
*   **Forfeit Match**: Type `q` at an attack prompt to abort execution safely.
*   **Screen Peeking Defences**: In local pass-and-play, the system issues black screen masks and prompts `"Begin turn..."` before revealing secret deployment maps.

### Visual Key
*   ` . ` (**Blue**): Untouched ocean water.
*   ` S ` (**Green**): Your healthy deployed ship units.
*   ` M ` (**Green**): Your registered miss markers (on your Hit Board).
*   ` G ` (**Orange**): Enemy missed guesses (on your Ship Board).
*   ` X ` (**Orange**): Your successful recorded hits.
*   ` # ` (**Red**): Wreckage of a fully **Sunk** ship.
