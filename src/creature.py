import math
import typing as tp
from dataclasses import dataclass, field
from random import randint

from loguru import logger

from parameters import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    Color,
    FACING_VARIATION,
    TICK_MOVE,
)
from position import Position
from utils import choose_with_probability
from virus import Virus


@dataclass
class Creature:
    """A creature descriptor object"""

    name: tp.Union[str, int]
    color: Color = COLOR_BLUE
    alive: bool = True
    position: Position = field(default_factory=lambda: Position())
    infected_remainder_ticks: int = 0
    virus: tp.Optional[Virus] = None
    immune_to: tp.Set[Virus] = field(default_factory=set)

    @property
    def is_sick(self) -> bool:
        return self.virus is not None

    def tick_update(self) -> None:
        if not self.alive:
            return

        self._move()
        self._update_virus_status()

    def _move(self) -> None:
        def get_new_position(facing: int) -> Position:
            return Position(
                facing=facing + randint(-FACING_VARIATION, FACING_VARIATION),
                x=int(self.position.x + math.cos(math.radians(facing)) * TICK_MOVE),
                y=int(self.position.y + math.sin(math.radians(facing)) * TICK_MOVE),
            )

        facing = self.position.facing
        position = get_new_position(facing)

        while not position.is_valid:
            facing = (facing + 60) % 360
            position = get_new_position(facing)

        self.position = position

    def _update_virus_status(self) -> None:
        if not self.is_sick:
            return

        assert self.virus is not None

        if self.infected_remainder_ticks > 0:
            self.infected_remainder_ticks -= 1

        if self.infected_remainder_ticks == 0:
            lethal_outcome: bool = choose_with_probability(self.virus.lethality)

            if lethal_outcome:
                self._die()
            else:
                self._cure()

    def _die(self) -> None:
        assert self.virus is not None
        self.alive = False
        self.color = COLOR_BLACK
        logger.info(f"{self.name} has died from {self.virus.name}")
        self.virus = None

    def _cure(self) -> None:
        assert self.virus is not None
        self.immune_to.add(self.virus)
        self.color = COLOR_GREEN
        logger.info(
            f"{self.name} has cured from {self.virus.name} and became immune to it"
        )
        self.virus = None

    def infect(self, virus: Virus) -> None:
        if self.is_sick or virus in self.immune_to:
            return

        if choose_with_probability(virus.contingency):
            self.infected_remainder_ticks = virus.lifetime
            self.color = COLOR_RED
            self.virus = virus
            logger.info(f"{self.name} has been infected with {virus.name}")
