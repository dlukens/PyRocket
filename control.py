import pygame
import pymunk
import math
import numpy as np

import ISAcalcmod
import objects

from pygame.locals import *

def camera(rocket, ground, gravity, rocket_empty_mass, rocket_fuel_mass, ceiling, screenx, space, gear):
    angle = pymunk.Body._get_angle(rocket.body)

    # Miscellaneous
    rocket_mass = rocket_empty_mass + rocket_fuel_mass
    pymunk.Body._set_mass(rocket.body, rocket_mass)
    pymunk.Body._set_mass(ground.body, rocket_mass)

    rocket_pos = -(pymunk.Body._get_position(ground.body)
                   [0] - screenx / 2), -(pymunk.Body._get_position(ground.body)[1] - 30)

    # Gravity fade
    gravity_init = 900
    gravity_end = 600
    gravity = (gravity_end - gravity_init) / \
        ceiling * rocket_pos[1] + gravity_init

    ground.body.apply_force_at_local_point(
        (0, ground.body._get_mass() * gravity), (0, 0))

    # drag
    air_density = ISAcalcmod.CALC((rocket_pos[1] * 86000) / (ceiling * 5))

    rocket_vel = - \
        ground.body._get_velocity()[0] / 100, - \
        ground.body._get_velocity()[1] / 100

    air_speed = math.hypot(rocket_vel[0], rocket_vel[1])
    air_speed_angle = math.atan2(rocket_vel[0], rocket_vel[1])

    AoA = air_speed_angle + angle

    surface_top = math.pi * (rocket.w/2)**2
    surface_side = rocket.w * rocket.h

    if gear:
        CD = 0.2 + 1.2 * abs(math.sin(AoA))
    else:
        CD = 0.1 + 1.2 * abs(math.sin(AoA))

    drag_force = 0.5 * CD * air_density * air_speed**2 * (surface_top + surface_side) * 20

    drag = [0,0]
    drag[0] = drag_force *(abs(math.sin(AoA)*math.sin(air_speed_angle))*-np.sign(rocket_vel[0]) + abs(math.sin(2 * AoA)*math.cos(air_speed_angle))*0.5*np.sign(math.sin(2*AoA)))
    drag[1] = drag_force *(abs(math.sin(AoA)*math.cos(air_speed_angle))*-np.sign(rocket_vel[1]) + abs(math.sin(2 * AoA)*math.sin(air_speed_angle))*0.5*np.sign(math.sin(2*AoA)))

    ground.body.apply_force_at_local_point((-drag[0], -drag[1]), (0, 0))
    rocket.body.apply_force_at_local_point((drag_force * math.sin(AoA)/4, 0), (0, rocket.w/2))


    return rocket_pos, rocket_mass, angle, air_density, air_speed_angle, gravity

def keys(space, rocket_fuel_mass, engine_massflow, ground, thrust, force_rcs, angle, rocket, joint1, joint2, leg1, leg2, gear, boom):
    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and rocket_fuel_mass - engine_massflow >= 0 and not boom:

        ground.body.apply_force_at_local_point(
            (thrust * math.sin(angle), -thrust * math.cos(angle)), (rocket.w / 2, 0))

        rocket_fuel_mass -= engine_massflow

    if keys[K_d] or keys[K_RIGHT] and not boom:
        rocket.body.apply_force_at_local_point(
            (force_rcs, 0), (rocket.w / 2, rocket.h))

        ground.body.apply_force_at_local_point(
            (-force_rcs * math.cos(angle) / 10, force_rcs * math.sin(angle) / 10), (0, 0))

    if keys[K_a] or keys[K_LEFT] and not boom:
        rocket.body.apply_force_at_local_point(
            (-force_rcs, 0), (rocket.w / 2, rocket.h))
        ground.body.apply_force_at_local_point(
            (force_rcs * math.cos(angle) / 10, -force_rcs * math.sin(angle) / 10), (0, 0))

    if keys[K_g] and not boom:

        joint1.rotary._set_rest_angle(math.pi / 4 * 3)
        joint2.rotary._set_rest_angle(-math.pi / 4 * 3)

        gear = True

    return(rocket_fuel_mass, gear)
