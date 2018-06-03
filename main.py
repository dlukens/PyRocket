import math
import sys
import random
import pygame
from pygame.locals import *

import labels
import control
import objects
import display
import game

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

launch = False

time = 0

# ---Space---
space = pymunk.Space()
draw_options = pymunk.pygame_util.DrawOptions(screen)

ceiling = 250000

gravity = 900

# ---Ground---
ground_h = 200
ground_w = 400000

ground_img = pygame.image.load('data/grass.jpg').convert_alpha()
ground_img = pygame.transform.scale(ground_img, (400, ground_h))

lz_offset = 100000

# ---Rocket---
rocket_fuel_mass_init = 800000
rocket_fuel_mass = rocket_fuel_mass_init
rocket_empty_mass = 150000

rocket_start_pos = ground_w/3

rocket_mass = rocket_empty_mass + rocket_fuel_mass

# engine_isp = 400
engine_isp = 600
engine_massflow = 80


force_rcs = 2e8

rocket, leg1, leg2, ground, joint1, joint2 = objects.begin(
    space, rocket_mass, screenx,screeny, ground_h, ground_w, rocket_start_pos)


# ---Main Loop---
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    if launch:
        time += dt

    thrust = engine_isp * engine_massflow * gravity * 30


    # ---Control---
    rocket_pos, rocket_mass, angle, air_density, air_speed_angle, drag_angle, gravity = control.camera(
        rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ceiling, screenx)

    launch, rocket_fuel_mass = control.keys(
        space, rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, launch, angle, rocket, joint1, joint2, leg1, leg2)

    landed, landed_timer, boom, out_map = game.logic(rocket, ground, rocket_pos, lz_offset, space, angle, ceiling)
    rocket_fuel_mass, launch, landed = game.restart(rocket_start_pos, ground, rocket, joint1, joint2, rocket_fuel_mass_init ,rocket_fuel_mass, launch, screen, landed)


    # ---Screen business---

    display.graphics(rocket_pos, screen, space, draw_options,
                     screeny, ground_img, ground, rocket, ceiling, lz_offset)

    display.GUI(screen, ground, screenx, rocket_pos, ceiling, rocket_start_pos, lz_offset, angle, air_speed_angle, drag_angle)

    labels.text(screen, rocket, ground, rocket_pos,
                thrust, gravity, time, air_density, rocket_start_pos, landed_timer)

    display.splash(landed, boom, out_map, screen, screenx)

    # Flip screen
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    # ---Physics---
    dt = 1 / 60.0

    space.step(dt)
