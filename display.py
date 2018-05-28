import pygame, math, pymunk

import pymunk.pygame_util
import numpy as np


def GUI(screen, ground, screenx, rocket_pos, ceiling):
    global time
    # minimap
    size = 160
    minimap = pygame.Surface((size, size))
    minimap.set_alpha(120)
    minimap.fill((100, 100, 100))

    unit_w = size / ground.w
    unit_h = size / ceiling

    minimap_ground = pygame.draw.rect(
        minimap, (255, 0, 0), (0, size - 4, size, 10))

    minimap_rocket_pos = [0, 0]
    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)

    minimap_rocket = pygame.draw.rect(minimap, (0, 0, 255), (
        minimap_rocket_pos[0] + size / 2, size - 6 - minimap_rocket_pos[1], 4, 4))

    minimap_lz_pos = [0, 0]
    minimap_lz_pos[0] = round((-ground.w/2 + lz_offset) * unit_w, 2)
    minimap_lz_pos[1] = round(lz_pos[1] * unit_h, 2)

    minimap_lz = pygame.draw.rect(minimap, (0, 255, 0), (
        minimap_lz_pos[0] + size / 2, size - 4 , lz_size[0]/ 100, 4))

    screen.blit(minimap, (screenx - size - 10, 10))


def graphics(rocket_pos, screen, space, draw_options, screeny, ground_img, ground, rocket, ceiling):
    global lz_pos, lz_size, lz_offset

    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([48 ,31, 93])

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
    #landing zone

    lz_offset = ground.w / 2

    lz_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + lz_offset, ground.body._get_position()[1] + ground.h), screen)
    lz_size = 600, 100

    pygame.draw.rect(screen, (255, 0, 0), (lz_pos[0], lz_pos[1], lz_size[0], lz_size[1] ))
