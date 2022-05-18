from dataclasses import dataclass, field
from random import randint

from parameters import FIELD_HEIGHT, FIELD_WIDTH


@dataclass(frozen=True)
class Position:
    """A position descriptor object"""

    x: int = field(
        default_factory=lambda: randint(0, FIELD_WIDTH)
    )
    y: int = field(
        default_factory=lambda: randint(0, FIELD_HEIGHT)
    )
    facing: int = field(
        default_factory=lambda: randint(0, 360)
    )

    @property
    def is_valid(self) -> bool:
        return (
            0 <= self.x <= FIELD_WIDTH
            and 0 <= self.y <= FIELD_HEIGHT
        )
