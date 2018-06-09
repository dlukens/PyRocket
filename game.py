import pygame, pymunk, math
from pygame.locals import *

clock = pygame.time.Clock()
timer = pygame.time.get_ticks
timeout = 3000 # milliseconds
deadline = timer() + timeout

landed = False

boom = False
out_map = False

def logic(rocket, ground, rocket_pos, lz_offset, space, angle, ceiling):
    global timeout, deadline, landed, boom, out_map
    now = timer()

    #Landing detection
    if math.radians(10) >= angle >= math.radians(-10):
        if rocket_pos[1] <= 100 and lz_offset <= rocket_pos[0] <= lz_offset + 20000:
            if now >= deadline:
                landed = True

        else:
            deadline = now + timeout
            landed = False
    else:
        deadline = now + timeout
        landed = False


    if deadline - now >= 0:
        landed_timer = (deadline - now)/1000
    elif landed:
        landed_timer = 'Ye'

    #out of map detection
    if now >= 1000 and rocket_pos[0] <= 0 or rocket_pos[0] >= ground.w or rocket_pos[1] >= ceiling:
        out_map = True
    else:
        out_map = False

    #body hit detection
    def coll_begin(arbiter, space, data):
        if arbiter.shapes[0].id == 2 and  arbiter.shapes[1].id == 0:
            print('boom')
            boom = True

        return True

    handler = space.add_default_collision_handler()
    handler.begin = coll_begin

    return landed, landed_timer, boom, out_map

def restart(rocket_start_pos, ground, rocket, joint1, joint2, rocket_fuel_mass_init, rocket_fuel_mass, screen, landed, gear):
    keys = pygame.key.get_pressed()
    if keys[K_r]:
        print('r')

        gear = False

        ground.body.position = (-rocket_start_pos, -100)
        ground.body.velocity = (0, 0)

        rocket.body.angle = 0
        rocket.body.angular_velocity = 0

        joint1.rotary._set_rest_angle(-math.pi/4 * 3)
        joint2.rotary._set_rest_angle(0)


        return rocket_fuel_mass_init, False, gear
    return rocket_fuel_mass, landed, gear
