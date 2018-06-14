import labels
import control
import objects
import display
import game

try:
    import pygame
except:
    print("Run pip install pygame")
    quit()

try:
    import pymunk
except:
    print("Run pip install pymunk")
    quit()

# ---Setup---
pygame.init()
screenx = 1000
screeny = 700
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()
running = True

# ---Space---
space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(screen)
draw_options.flags = draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_CONSTRAINTS

ceiling = 500000

gravity = 700

# ---Ground---
ground_h = 300
ground_w = 1200000

lz_offset = 80000

# ---Rocket---
rocket_fuel_mass_init = 480000
rocket_fuel_mass = rocket_fuel_mass_init
rocket_empty_mass = 100000

rocket_start_pos = ground_w - 10000

rocket_mass = rocket_empty_mass + rocket_fuel_mass_init

engine_isp = 800 * 9
engine_massflow_init = 84

# Game variables

gear = False
boom = False

display.imageinit(ground_w, ground_h, screenx, screeny)

rocket, ground, joint1, joint2, rocket_joint, cloud = objects.begin(
    space, rocket_mass, screenx, screeny, ground_h, ground_w, rocket_start_pos, screen)

with open('scores.dat', 'r') as file:
    lines = file.readlines()

    last_time = lines[0]
    best_time = lines[1]

lz_size = 3, 0
isle_number = 3

# ---Main Loop---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Thrust
    if gear:
        engine_massflow = engine_massflow_init / 3
        force_rcs = 9e7
    else:
        engine_massflow = engine_massflow_init
        force_rcs = 7e7

    thrust = engine_isp * engine_massflow * gravity

    # CoM calc
    com_init = rocket.h / 2
    com_end = rocket.h / 4
    rocket_joint.anchor_a = rocket.w/2, (com_end-com_init) / \
        (rocket_empty_mass-950000)*(rocket_mass-950000) + com_init

    # ---Control---
    rocket_pos, rocket_mass, angle, air_density, air_speed_angle, gravity = control.camera(
        rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ceiling, screenx, gear)

    rocket_fuel_mass, gear = control.keys(
        rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, angle, rocket, joint1, joint2, gear, boom)

    game.score()

    landed, boom, out_map, launched, time, above = game.logic(
        ground, rocket_pos, lz_offset, space, angle, ceiling, lz_size, isle_number)
    rocket_fuel_mass, landed, gear, launched, last_time, best_time = game.restart(
        rocket_start_pos, ground, rocket, joint1, joint2, rocket_fuel_mass_init, rocket_fuel_mass, landed, gear, last_time, best_time)

    # ---Screen business---
    lz_size, isle_number = display.graphics(rocket_pos, screen, space, draw_options,
                                            screeny, ground, ceiling, lz_offset, rocket_start_pos, screenx, rocket_joint, rocket, angle)

    display.GUI(screen, ground, screenx, rocket_pos, ceiling, lz_offset, angle,
                air_speed_angle, rocket_start_pos, screeny, rocket_fuel_mass_init, rocket_fuel_mass, rocket)

    labels.text(screen, rocket, ground, rocket_pos,
                thrust, gravity, air_density, rocket_empty_mass, screeny, time, last_time, best_time, above)

    display.splash(landed, boom, out_map, screen, rocket_fuel_mass, screenx, screeny)

    for i in range(cloud.number):# only render visible clouds

        cloudpos = (cloud.list[i][0] - rocket_pos[0], cloud.list[i][1] + rocket_pos[1])

        if cloud.list[i][0] >= rocket_pos[0] - cloud.max_len and cloud.list[i][0] <= rocket_pos[0] + screenx:
            if -cloud.list[i][1] <= rocket_pos[1] + cloud.max_he and -cloud.list[i][1] >= rocket_pos[1] - screeny:
                screen.blit(cloud.imglist[i], cloudpos)

    display.infoscreen(screenx, screeny, screen)

    # Flip screen
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    # ---Physics---
    dt = 1 / 60.0

    space.step(dt)
