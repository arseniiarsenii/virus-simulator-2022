import math
import typing as tp
from random import randint

from position import Position


def choose_with_probability(probability: tp.Union[int, float]) -> bool:
    """Chose with certain probability"""
    if isinstance(probability, float):
        probability = int(probability * 100)

    return randint(0, 100) <= probability


def get_distance(pos_1: Position, pos_2: Position) -> float:
    """Get distance between two given points`"""
    x_dist = abs(pos_1.x - pos_2.x)
    y_dist = abs(pos_1.y - pos_2.y)
    return math.sqrt(x_dist**2 + y_dist**2)
