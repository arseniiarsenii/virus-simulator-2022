import sys
import time
from itertools import cycle

import pygame
from loguru import logger

import utils
from creature import prepare_creatures
from parameters import (
    COLOR_BLACK,
    COLOR_WHITE,
    CREATURE_COUNT,
    FIELD_HEIGHT,
    FIELD_WIDTH,
    VIRUSES,
)
from stats import Stats

pygame.init()
SCREEN = pygame.display.set_mode(
    (FIELD_WIDTH, FIELD_HEIGHT)
)
pygame.display.set_caption("VIRUS SIMULATOR")
viruses = cycle(VIRUSES)
virus = next(viruses)
CREATURES = prepare_creatures(virus)
running = True
STATS = Stats()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not running:
        continue

    SCREEN.fill(COLOR_WHITE)
    STATS.tick_cnt += 1

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

            for j in filter(
                lambda x: CREATURES[x].is_recipient,
                range(CREATURE_COUNT),
            ):
                distance = utils.get_distance(
                    creature.position, CREATURES[j].position
                )

                if (
                    distance
                    <= creature.virus.transmission_radius
                    and CREATURES[j].alive
                ):
                    CREATURES[j].infect(creature.virus)

            STATS.sick += 1
        elif not creature.alive:
            STATS.dead += 1
        elif creature.immune_to:
            STATS.cured += 1
        else:
            STATS.healthy += 1

        pygame.draw.circle(
            SCREEN,
            creature.color,
            (creature.position.x, creature.position.y),
            10,
        )

    font_size = 20
    font = pygame.font.SysFont("Arial", font_size)
    stats = font.render(
        str(STATS), True, COLOR_BLACK, COLOR_WHITE
    )
    SCREEN.blit(stats, (20, 20))
    virus_name = font.render(
        virus.name, True, COLOR_BLACK, COLOR_WHITE
    )
    SCREEN.blit(
        virus_name, (20, FIELD_HEIGHT - 20 - font_size)
    )
    pygame.display.update()

    if STATS.sick == 0:
        logger.info(
            "No sick creatures left. Collective immunity achieved"
        )
        running = False

    if STATS.dead == CREATURE_COUNT:
        logger.info("All creatures have died")
        running = False

    if not running:
        virus = next(viruses)
        CREATURES = prepare_creatures(virus)
        running = True
        STATS = Stats()
        time.sleep(5)

    STATS.reset_cnt()

    time.sleep(0.01)
