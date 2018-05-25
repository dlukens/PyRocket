import math, sys, random

import labels, interface, control, objects

import numpy as np

import pygame
from pygame.locals import *
from pygame.color import *

try:
    import pymunk
except:
    print("Run pip install pymunk")
    quit()

import pymunk.pygame_util

# ---Set-up---
pygame.init()
screenx = 1000
screeny = 700
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()
running = True

launch = False

# ---Space---
space = pymunk.Space()

draw_options = pymunk.pygame_util.DrawOptions(screen)

gravity = 900

ceiling = 240000

# ---Ground---
ground_h = 200
ground_w = 800000

ground_img = pygame.image.load('data/grass.jpg').convert_alpha()
ground_img = pygame.transform.scale(ground_img, (200, ground_h))

# ---Rocket---
rocket_fuel_mass = 400000
rocket_empty_mass = 140000

rocket_mass = rocket_empty_mass + rocket_fuel_mass

engine_isp = 330
engine_massflow = 110

thrust = engine_isp * engine_massflow * gravity * 14
force_rcs = 2e7


rocket, leg1, leg2, ground, joint1, joint2 = objects.begin(
    space, rocket_mass, screenx, ground_h, ground_w)


# ---Main Loop---
while running:
    for event in pygame.event.get():                                            # Exit program
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    rocket_pos, rocket_mass, angle = control.camera(
        rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ground_w)

    launch, rocket_fuel_mass = control.keys(
        rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, launch, angle, rocket)

    # ---Screen display---
    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([10, 1, 46])

    sky_color_diff = sky_color_ground - sky_color_space

    # function to exponentially change bg color
    color_step = sky_color_diff * \
        (math.exp(rocket_pos[1] * math.log(2) / ceiling) - 1)

    bg_color = abs(sky_color_ground - color_step)

    screen.fill(bg_color)

    space.debug_draw(draw_options)

    # ground image
    if rocket_pos[1] < screeny / 2:  # prevent weird repeating pattern
        for len in range(0, ground_w, 1400):
            screen.blit(ground_img, pymunk.pygame_util.to_pygame((ground.body._get_position()[0]
                                        + len, ground.body._get_position()[1] + ground_h), screen))

    interface.GUI(screen, ground_w, ceiling, screenx, rocket_pos)

    labels.text(screen, rocket.body, ground.body, rocket_pos, thrust, gravity)

    # Flip screen
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    # ---Physics---
    dt = 1 / 60.0
    space.step(dt)
