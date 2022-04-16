import typing as tp

import virus

# Configuration
FIELD_HEIGHT = 1000
FIELD_WIDTH = 2000
CREATURE_COUNT = 100
INFECTED_INIT_COUNT = 3
TICK_MOVE = 5
FACING_VARIATION = 30
VIRUSES = [virus.virus_1, virus.virus_2, virus.virus_3]

# Colors
Color = tp.Tuple[int, int, int]
COLOR_BLACK: Color = (0, 0, 0)
COLOR_RED: Color = (255, 0, 0)
COLOR_GREEN: Color = (0, 255, 0)
COLOR_BLUE: Color = (0, 0, 255)
COLOR_WHITE: Color = (255, 255, 255)
