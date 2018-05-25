import pygame
import pymunk
import math
from pygame.locals import *


def camera(rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ground_w):
    rocket.body.velocity = (0, 0)
    angle = pymunk.Body._get_angle(rocket.body)

    if pymunk.Body._get_position(ground.body)[1] < 80:  # Avoid weird floating
        ground.body.apply_force_at_local_point(
            (0, ground.body._get_mass() * gravity), (0, 0))

    # Miscellaneous
    rocket_mass = rocket_empty_mass + rocket_fuel_mass
    pymunk.Body._set_mass(rocket.body, rocket_mass)
    pymunk.Body._set_mass(ground.body, rocket_mass)

    rocket_pos = -(pymunk.Body._get_position(ground.body)
                   [0] + ground_w / 2), -(pymunk.Body._get_position(ground.body)[1] - 30)

    return(rocket_pos, rocket_mass, angle)


def keys(rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, launch, angle, rocket):
    keys = pygame.key.get_pressed()
    if keys[K_w] or launch:
        ground.body.apply_force_at_local_point(
            (thrust * math.sin(angle), -thrust * math.cos(angle)), (rocket.w / 2, 0))

        rocket_fuel_mass -= engine_massflow

    if keys[K_d]:
        rocket.body.apply_force_at_local_point(
            (force_rcs, 0), (rocket.w / 2, rocket.h))

    if keys[K_a]:
        rocket.body.apply_force_at_local_point(
            (-force_rcs, 0), (rocket.w / 2, rocket.h))

    if keys[K_SPACE]:
        launch = True

    return(launch, rocket_fuel_mass)
