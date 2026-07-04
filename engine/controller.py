from abc import ABC, ABCMeta, abstractmethod
from engine.player import Player
from ai.bot import BattleshipAI
from engine.ui import get_ship_placement

class Controller(ABC):
    def __init__(self, player_obj: Player) -> None:
        self.player = player_obj
    
    @abstractmethod
    def deploy_fleet(self, fleet: list[tuple[str, int]]) -> None:
        pass

    @abstractmethod
    def get_move(self) -> tuple[int, int] | str:
        pass

    @abstractmethod
    def register_result(self, x: int, y: int, result: str) -> None:
        pass

class HumanController(Controller):
    def deploy_fleet(self, fleet_manifest: list[tuple[str, int]]) -> None:
        for name, length in fleet_manifest:
            get_ship_placement(self.player, name, length)

    def get_move(self) -> tuple[int, int] | str:
        user_input = input("Enter attack coordinates as 'x y' (or 'q' to quit) > ").strip()
        if user_input.lower() == "q":
            return "q"
        try:
            x, y = user_input.split()
            return int(x), int(y)
        except ValueError:
            return "invalid_format"

    def register_result(self, x: int, y: int, result: str) -> None:
        # Human just sees the printed message on screen via the main loop
        pass


class AIController(Controller):
    def __init__(self, player_obj: Player, ai_backend: BattleshipAI) -> None:
        super().__init__(player_obj)
        self.ai = ai_backend
        self.player = ai_backend.player_profile

    def deploy_fleet(self, fleet_manifest: list[tuple[str, int]]) -> None:
        self.ai.auto_deploy_fleet(fleet_manifest)

    def get_move(self) -> tuple[int, int] | str:
        # Automatically calculates its next attack coordinate
        return self.ai.calculate_next_move()

    def register_result(self, x: int, y: int, result: str) -> None:
        # Feeds the result back into its target queue memory bank
        self.ai.process_shot_result(x, y, result)