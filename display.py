import pygame, math, pymunk

import pymunk.pygame_util
import numpy as np


ceiling = 240000


def GUI(screen, ground_w, screenx, rocket_pos):
    global time
    # minimap
    size = 160
    minimap = pygame.Surface((size, size))
    minimap.set_alpha(120)
    minimap.fill((100, 100, 100))

    unit_w = size / ground_w
    unit_h = size / ceiling

    minimap_rocket_pos = [0, 0]

    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)

    minimap_ground = pygame.draw.rect(
        minimap, (255, 0, 0), (0, size - 4, size, 10))

    minimap_rocket = pygame.draw.rect(minimap, (100, 150, 200), (
        minimap_rocket_pos[0] + size / 2, size - 6 - minimap_rocket_pos[1], 4, 4))

    screen.blit(minimap, (screenx - size - 10, 10))



def graphics(rocket_pos, screen, space, draw_options, screeny, ground_img, ground):
    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([10, 1, 46])

    sky_color_diff = sky_color_ground - sky_color_space

    color_step = sky_color_diff * \
        (math.exp(rocket_pos[1] * math.log(2) / ceiling) - 1) # function to exponentially change bg color

    bg_color = abs(sky_color_ground - color_step)

    screen.fill(bg_color)

    space.debug_draw(draw_options)


    if rocket_pos[1] < screeny / 2:  # prevent weird repeating pattern
        for len in range(0, ground.w, 1400):
            screen.blit(ground_img, pymunk.pygame_util.to_pygame((ground.body._get_position()[0]
                                        + len, ground.body._get_position()[1] + ground.h), screen))
