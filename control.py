import pygame, pymunk, math

import ISAcalcmod, objects

from pygame.locals import *


def camera(rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ceiling, screenx):
    angle = pymunk.Body._get_angle(rocket.body)

    ground.body.apply_force_at_local_point((0, ground.body._get_mass() * gravity), (0, 0))

    # Miscellaneous
    rocket_mass = rocket_empty_mass + rocket_fuel_mass
    pymunk.Body._set_mass(rocket.body, rocket_mass)
    pymunk.Body._set_mass(ground.body, rocket_mass)

    rocket_pos = -(pymunk.Body._get_position(ground.body)
                   [0] - screenx/2), -(pymunk.Body._get_position(ground.body)[1] - 30)

    #drag
    air_density = ISAcalcmod.CALC((rocket_pos[1]*86000)/(ceiling*10))

    rocket_vel = -ground.body._get_velocity()[0]/10, -ground.body._get_velocity()[1]/10

    dragy = 0.5 * 0.5 * air_density * rocket_vel[1]**2 * 100
    # print(dragy)

    return(rocket_pos, rocket_mass, angle, air_density)


def keys(space, rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, launch, angle, rocket, joint1, joint2, leg1, leg2):
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

    if keys[K_g]:

        joint1.rotary._set_rest_angle(math.pi/4 * 3)
        joint2.rotary._set_rest_angle(-math.pi/4 * 3)


    return(launch, rocket_fuel_mass)
