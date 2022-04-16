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


virus_1 = Virus(
    name="Virus 1",
    infectiousness=0.9,
    lethality=0.01,
    transmission_radius=50,
    lifetime=100,
)

virus_2 = Virus(
    name="Virus 2",
    infectiousness=0.95,
    lethality=0.02,
    transmission_radius=120,
    lifetime=140,
)

virus_3 = Virus(
    name="Virus 3",
    infectiousness=0.95,
    lethality=0.12,
    transmission_radius=70,
    lifetime=170,
)
