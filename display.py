import pygame, math, pymunk

import pymunk.pygame_util
import numpy as np

minimap_rocket_pos_history = [[0,0], [0,0]]
minimap_trail = [[0,0]]
minimap_trail_color = [[0, 0, 0]]

def GUI(screen, ground, screenx, rocket_pos, ceiling, rocket_start_pos, lz_offset, angle, air_speed_angle, lp_offset, screeny, rocket_fuel_mass_init, rocket_fuel_mass, rocket):
    global time
    # minimap
    size_x = 360
    size_y = 200
    minimap = pygame.Surface((size_x, size_y))
    minimap.set_alpha(120)
    minimap.fill((100,100,100))

    unit_w = size_x / ground.w
    unit_h = size_y / ceiling

    minimap_ground = pygame.draw.rect(
        minimap, (200, 0, 100), (0, size_y - 4, size_x, 10))

    minimap_rocket_pos = [0, 0]
    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)

    minimap_rocket_pos_history.append(minimap_rocket_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        trail_color = (226, 192, 68)
    else:
        trail_color = (100,0,150)

    if round(minimap_rocket_pos_history[-1][0], 1) != round(minimap_rocket_pos_history[-2][0], 1):
        if round(minimap_rocket_pos_history[-1][1], 1) != round(minimap_rocket_pos_history[-2][1], 1):
            minimap_trail.append(minimap_rocket_pos)
            minimap_trail_color.append(trail_color)


    for i in range(len(minimap_trail)):
        pygame.draw.rect(minimap, minimap_trail_color[i], (
            minimap_trail[i][0], size_y - 6 - minimap_trail[i][1], 1, 1))


    minimap_rocket = pygame.draw.rect(minimap, (0, 0, 255), (
        minimap_rocket_pos[0], size_y - 6 - minimap_rocket_pos[1], 4, 4))

    minimap_lz_pos = round((lz_offset - ground.w/2) * unit_w, 2)

    minimap_lz = pygame.draw.rect(minimap, (0, 255, 0), (
        minimap_lz_pos + size_x / 2, size_y - 4 , lz_size[0]*isle_number/ 4000, 4))

    minimap_lp_pos = round((lp_offset - ground.w/2) * unit_w, 2)

    minimap_lp = pygame.draw.rect(minimap, (0, 100, 255), (
        minimap_lp_pos + size_x / 2, size_y - 4 , lp_size[0]/ 4000, 4))


    screen.blit(minimap, (screenx - size_x - 10, 10))

    #compass

    compass_heading_pos = [round(screenx/2 + 160 * math.sin(-angle)), round(400 - rocket.w/2 - 160 * math.cos(angle))]
    pygame.draw.circle(screen, (0, 255, 0), compass_heading_pos, 5)

    compass_airspeed_pos = [round(screenx/2 + 160 * math.sin(air_speed_angle)), round(400 - rocket.w/2 - 160 * math.cos(air_speed_angle))]
    pygame.draw.circle(screen, (255, 0, 0), compass_airspeed_pos, 5)

    # Interface
    pygame.draw.rect(screen, (159, 177, 188), (0, screeny - 20, screenx, 20))
    pygame.draw.rect(screen, (226, 192, 68), (820, screeny - 20, 200, 20))
    pygame.draw.rect(screen, (211, 208, 203), (670, screeny - 20, 150, 20))


    pygame.draw.circle(screen, (255, 0, 0), (10, screeny - 10), 5)
    pygame.draw.circle(screen, (0, 255, 0), (120, screeny - 10), 5)

    pygame.draw.rect(screen, (211, 208, 203), (10, 10, 300, 200))

    pygame.draw.rect(screen, (226, 192, 68), (20, 180, 280, 20))
    fuel_left = 280/rocket_fuel_mass_init * rocket_fuel_mass
    pygame.draw.rect(screen, (159, 177, 188), (20, 180, fuel_left, 20))


def imageinit(ground_w, ground_h, screenx, screeny):
    global sand_limit, water_limit, ground_img, water_img, sand_list, water_list, sand_w, water_w, launchpad_img, isle_img, info_img

    ground_img = pygame.image.load('data/sand.jpg').convert_alpha()
    ground_img = pygame.transform.scale(ground_img, (2000, ground_h))

    launchpad_img = pygame.image.load('data/launchpad.png').convert_alpha()
    launchpad_img = pygame.transform.scale(launchpad_img, (2000, 250))

    isle_img = pygame.image.load('data/isle.png').convert_alpha()
    isle_img = pygame.transform.scale(isle_img, (16000, 600))

    info_img = pygame.image.load('data/info.jpg').convert_alpha()
    info_img = pygame.transform.scale(info_img, (screenx, screeny))

    sand_limit = int(ground_w - 12000), int(ground_w)
    water_limit = int(0), int(sand_limit[0])

    sand_w = ground_img.get_rect().size[0]

    sand_list = [(0,0)] * int((sand_limit[1] - sand_limit[0])/sand_w)

def graphics(rocket_pos, screen, space, draw_options, screeny, ground, rocket, ceiling, lz_offset, lp_offset, screenx):
    global lz_pos, lz_size, lp_pos, lp_size, isle_number

    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([48 ,31, 93])

    sky_color_diff = sky_color_ground - sky_color_space

    color_step = sky_color_diff * \
        (math.exp(rocket_pos[1] * math.log(2) / ceiling) - 1) # function to exponentially change bg color

    if rocket_pos[1] <= ceiling:
        bg_color = abs(sky_color_ground - color_step)
    else:
        bg_color = sky_color_space

    screen.fill(bg_color)

    space.debug_draw(draw_options)

    #ground images

    if rocket_pos[1] < screeny:

        #water
        water_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0], ground.body._get_position()[1] + ground.h), screen)
        pygame.draw.rect(screen, (0,0,255), (water_pos[0], water_pos[1], ground.w, ground.h))

        # sand
        for i in range(len(sand_list)):
            sand_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + sand_limit[0] + i*sand_w, ground.body._get_position()[1] + ground.h), screen)
            sand_list[i] = sand_pos

            if sand_limit[0] - screenx/2 <= rocket_pos[0] <= sand_limit[1] + screenx/2:      #fix weird pattern
                screen.blit(ground_img, sand_list[i])

        #isle
        lz_size = isle_img.get_rect().size
        isle_number = 3

        for i in range(isle_number):
            lz_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + lz_offset + i*lz_size[0], ground.body._get_position()[1] + ground.h + 200), screen)

            if lz_offset - screenx <= rocket_pos[0] <= lz_offset + lz_size[0]*isle_number + screenx:
                screen.blit(isle_img, lz_pos)

        # launchpad
        lp_pos = pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + lp_offset - 600, ground.body._get_position()[1] + ground.h + 150), screen)
        lp_size = 2000, 100

        if rocket_pos[0] >= ground.w - 20000:

            screen.blit(launchpad_img, lp_pos)

    return lz_size, isle_number


def splash(landed, boom, out_map, screen, screenx, rocket_fuel_mass):
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

    if rocket_fuel_mass <= 0:
        splashy('You ran out of fuel!', (255, 122, 48))

infoshow = True

def infoscreen(screenx, screeny, screen):
    global infoshow

    mousepos = pygame.mouse.get_pos()
    mouseclick = pygame.mouse.get_pressed()[0]

    if infoshow:
        screen.blit(info_img, (0,0))

        if 260 <= mousepos[0] <= 730 and 500 <= mousepos[1] <= 650 and mouseclick:
            infoshow = False
