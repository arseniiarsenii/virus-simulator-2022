import sys
import time
from itertools import count

import pygame
from loguru import logger

import utils
from creature import Creature
from parameters import (
    COLOR_BLACK,
    COLOR_WHITE,
    CREATURE_COUNT,
    FIELD_HEIGHT,
    FIELD_WIDTH,
    INFECTED_INIT_COUNT,
    VIRUS,
)

CREATURES = [Creature(name=f"Creature {i}") for i in range(1, CREATURE_COUNT + 1)]

for i in range(INFECTED_INIT_COUNT):
    CREATURES[i].infect(VIRUS)

pygame.init()
SCREEN = pygame.display.set_mode((FIELD_WIDTH, FIELD_HEIGHT))
pygame.display.set_caption("VIRUS SIMULATOR")

for tick_cnt in count(1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill(COLOR_WHITE)

    healthy = 0
    sick = 0
    cured = 0
    dead = 0

    for i in range(CREATURE_COUNT):
        CREATURES[i].tick_update()
        creature = CREATURES[i]

        if creature.is_sick:
            assert creature.virus is not None

            pygame.draw.circle(
                SCREEN,
                COLOR_BLACK,
                (creature.position.x, creature.position.y),
                creature.virus.transmission_radius,
                1,
            )

            for j in range(CREATURE_COUNT):
                if i == j:
                    continue

                distance = utils.get_distance(creature.position, CREATURES[j].position)

                if (
                    distance <= creature.virus.transmission_radius
                    and CREATURES[j].alive
                ):
                    CREATURES[j].infect(creature.virus)

            sick += 1
        elif not creature.alive:
            dead += 1
        elif creature.immune_to:
            cured += 1
        else:
            healthy += 1

        pygame.draw.circle(
            SCREEN, creature.color, (creature.position.x, creature.position.y), 10
        )

    if sick == 0:
        logger.info("No sick creatures left. Collective immunity achieved")
    if dead == CREATURE_COUNT:
        logger.info("All creatures have died")

    status = "; ".join(
        [
            f"Tick {tick_cnt}",
            f"Healthy creatures: {healthy}",
            f"Sick creatures: {sick}",
            f"Cured creatures: {cured}",
            f"Dead creatures: {dead}",
            f"Total creatures: {CREATURE_COUNT}",
        ]
    )
    font = pygame.font.SysFont("Arial", 18)
    img = font.render(status, True, COLOR_BLACK, COLOR_WHITE)
    SCREEN.blit(img, (20, 20))

    time.sleep(0.05)
    pygame.display.update()
