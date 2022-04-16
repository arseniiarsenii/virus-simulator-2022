from dataclasses import dataclass

from parameters import CREATURE_COUNT


@dataclass
class Stats:
    tick_cnt: int = 0
    healthy: int = 0
    sick: int = 0
    cured: int = 0
    dead: int = 0
    total: int = CREATURE_COUNT

    def __str__(self) -> str:
        return "; ".join(
            [
                f"Tick {self.tick_cnt}",
                f"Healthy creatures: {self.healthy}",
                f"Sick creatures: {self.sick}",
                f"Cured creatures: {self.cured}",
                f"Dead creatures: {self.dead}",
                f"Total creatures: {self.total}",
            ]
        )

    def reset_cnt(self) -> None:
        self.healthy = 0
        self.sick = 0
        self.cured = 0
        self.dead = 0
