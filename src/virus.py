import typing as tp
from dataclasses import dataclass


@dataclass(frozen=True)
class Virus:
    """A virus descriptor object"""

    name: str
    infectiousness: float
    lethality: float
    transmission_radius: tp.Union[int, float]
    lifetime: int


influenza = Virus(
    name="Influenza",
    infectiousness=0.9,
    lethality=0.6,
    transmission_radius=100,
    lifetime=50,
)
