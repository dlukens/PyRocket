import pygame, math, pymunk

import pymunk.pygame_util
import numpy as np

minimap_rocket_pos_history = [[0,0], [0,0]]
minimap_trail = [[0,0]]

def GUI(screen, ground, screenx, rocket_pos, ceiling, rocket_start_pos, lz_offset, angle, air_speed_angle, lp_offset):
    global time
    # minimap
    size_x = 300
    size_y = 160
    minimap = pygame.Surface((size_x, size_y))
    minimap.set_alpha(120)
    minimap.fill((100, 100, 100))

    unit_w = size_x / ground.w
    unit_h = size_y / ceiling

    minimap_ground = pygame.draw.rect(
        minimap, (255, 0, 0), (0, size_y - 4, size_x, 10))

    minimap_rocket_pos = [0, 0]
    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)

    minimap_rocket_pos_history.append(minimap_rocket_pos)

    if round(minimap_rocket_pos_history[-1][0], 1) != round(minimap_rocket_pos_history[-2][0], 1):
        if round(minimap_rocket_pos_history[-1][1], 1) != round(minimap_rocket_pos_history[-2][1], 1):
            minimap_trail.append(minimap_rocket_pos)

    for i in range(len(minimap_trail)):
        pygame.draw.rect(minimap, (100,0,150), (
            minimap_trail[i][0], size_y - 6 - minimap_trail[i][1], 1, 1))


    minimap_rocket = pygame.draw.rect(minimap, (0, 0, 255), (
        minimap_rocket_pos[0], size_y - 6 - minimap_rocket_pos[1], 4, 4))

    minimap_lz_pos = round((lz_offset - ground.w/2) * unit_w, 2)

    minimap_lz = pygame.draw.rect(minimap, (0, 255, 0), (
        minimap_lz_pos + size_x / 2, size_y - 4 , lz_size[0]/ 4000, 4))

    minimap_lp_pos = round((lp_offset - ground.w/2) * unit_w, 2)

    minimap_lp = pygame.draw.rect(minimap, (0, 100, 255), (
        minimap_lp_pos + size_x / 2, size_y - 4 , lp_size[0]/ 4000, 4))


    screen.blit(minimap, (screenx - size_x - 10, 10))

    #compass
    # pygame.draw.circle(screen, (0, 0, 0), [500, 400], 150, 1)

    compass_heading_pos = [round(screenx/2 + 160 * math.sin(-angle)), round(400 - 160 * math.cos(angle))]
    pygame.draw.circle(screen, (250, 120, 200), compass_heading_pos, 5)

    compass_airspeed_pos = [round(screenx/2 + 160 * math.sin(air_speed_angle)), round(400 - 160 * math.cos(air_speed_angle))]
    pygame.draw.circle(screen, (200, 50, 200), compass_airspeed_pos, 5)


def graphics(rocket_pos, screen, space, draw_options, screeny, ground_img, ground, rocket, ceiling, lz_offset, lp_offset):
    global lz_pos, lz_size, lp_pos, lp_size

    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([48 ,31, 93])

    sky_color_diff = sky_color_ground - sky_color_space

    color_step = sky_color_diff * \
        (math.exp(rocket_pos[1] * math.log(2) / ceiling) - 1) # function to exponentially change bg color

    bg_color = abs(sky_color_ground - color_step)

    screen.fill(bg_color)

    space.debug_draw(draw_options)

    if rocket_pos[1] < screeny / 2:  # prevent weird repeating pattern
        for len in range(0, ground.w, 5000):
            screen.blit(ground_img, pymunk.pygame_util.to_pygame((ground.body._get_position()[0]
                                        + len, ground.body._get_position()[1] + ground.h), screen))
    #landing zone

    lz_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + lz_offset, ground.body._get_position()[1] + ground.h), screen)
    lz_size = 20000, 100

    pygame.draw.rect(screen, (255, 0, 200), (lz_pos[0], lz_pos[1], lz_size[0], lz_size[1] ))

    # launchpad

    lp_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + lp_offset, ground.body._get_position()[1] + ground.h), screen)
    lp_size = 2000, 100

    pygame.draw.rect(screen, (0, 100, 255), (lp_pos[0], lp_pos[1], lp_size[0], lp_size[1] ))



def splash(landed, boom, out_map, screen, screenx):
    def splashy(type, color):
        myfont = pygame.font.SysFont("monospace", 20)
        pygame.draw.rect(screen, color, (380, 20, 240, 100))

        label = myfont.render('{}'.format(type), 2, (0, 0, 0))
        label_restart = myfont.render('Press R to restart.', 2, (0, 0, 0))
        screen.blit(label, (390, 30))
        screen.blit(label_restart, (390, 80))



    if landed:
        splashy('You won!',(0, 255, 0))

    if boom:
        splashy('You exploded!',(255, 0, 0))

    if out_map:
        splashy('You left the map!',(255, 0, 100))
