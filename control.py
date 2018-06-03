import pygame
import pymunk
import math
import numpy as np

import ISAcalcmod
import objects

from pygame.locals import *


def camera(rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ceiling, screenx):
    angle = pymunk.Body._get_angle(rocket.body)



    # Miscellaneous
    rocket_mass = rocket_empty_mass + rocket_fuel_mass
    pymunk.Body._set_mass(rocket.body, rocket_mass)
    pymunk.Body._set_mass(ground.body, rocket_mass)

    rocket_pos = -(pymunk.Body._get_position(ground.body)
                   [0] - screenx / 2), -(pymunk.Body._get_position(ground.body)[1] - 30)

    #Gravity fade
    gravity_init = 900
    gravity_end = 100
    gravity = (gravity_end - gravity_init)/ceiling * rocket_pos[1] + gravity_init

    ground.body.apply_force_at_local_point(
        (0, ground.body._get_mass() * gravity), (0, 0))

    # drag
    air_density = ISAcalcmod.CALC((rocket_pos[1] * 86000) / (ceiling * 10))

    rocket_vel = - \
        ground.body._get_velocity()[0] / 100, - \
        ground.body._get_velocity()[1] / 100

    air_speed = math.sqrt(rocket_vel[0]**2 + rocket_vel[1]**2)
    air_speed_angle = math.atan2(rocket_vel[0], rocket_vel[1])

    delta_angle = air_speed_angle + angle

    surface_top = math.pi * 10**2
    surface_side = 100 * 20

    Cd = 0.8

    drag_force = abs(Cd * 0.5 * air_density * air_speed**2 * (abs(math.cos(
        delta_angle) * surface_top) + abs(math.sin(delta_angle) * surface_side)))

    drag = round(drag_force * math.sin(2 * delta_angle) * np.sign(rocket_vel[1])),  (- abs(math.cos(
        delta_angle)) * 1000 + round(drag_force * abs(math.sin(delta_angle))) * np.sign(rocket_vel[1]))

    drag_angle = math.atan2(drag[1], drag[0])

    ground.body.apply_force_at_local_point(
        (drag[0] * 200, drag[1] * 100), (0, 0))



    return rocket_pos, rocket_mass, angle, air_density, air_speed_angle, drag_angle, gravity


def keys(space, rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, launch, angle, rocket, joint1, joint2, leg1, leg2):
    keys = pygame.key.get_pressed()
    if keys[K_w] or launch:
        ground.body.apply_force_at_local_point(
            (thrust * math.sin(angle), -thrust * math.cos(angle)), (rocket.w / 2, 0))

        rocket_fuel_mass -= engine_massflow

    if keys[K_d]:
        rocket.body.apply_force_at_local_point(
            (force_rcs, 0), (rocket.w / 2, rocket.h))

        ground.body.apply_force_at_local_point(
            (-force_rcs * math.cos(angle) / 10, force_rcs * math.sin(angle) / 10), (0, 0))

    if keys[K_a]:
        rocket.body.apply_force_at_local_point(
            (-force_rcs, 0), (rocket.w / 2, rocket.h))
        ground.body.apply_force_at_local_point(
            (force_rcs * math.cos(angle) / 10, -force_rcs * math.sin(angle) / 10), (0, 0))

    if keys[K_SPACE]:
        launch = True

    if keys[K_g]:

        joint1.rotary._set_rest_angle(math.pi / 4 * 3)
        joint2.rotary._set_rest_angle(-math.pi / 4 * 3)

    return(launch, rocket_fuel_mass)
