import pygame, pymunk, math
from pygame.locals import *

clock = pygame.time.Clock()
timer = pygame.time.get_ticks
timeout = 3000 # milliseconds
deadline = timer() + timeout

landed = False

boom = False
out_map = False

launched = False
time = 0

def logic(rocket, ground, rocket_pos, lz_offset, space, angle, ceiling, lz_size, isle_number):
    global timeout, deadline, landed, out_map, launched, time, above
    now = timer()

    # launch detection
    if rocket_pos[1] >= 100:
        launched = True

    if launched and not landed:
        time += 1/60
    elif not launched:
        time = 0

    if lz_offset <= rocket_pos[0] <= lz_offset + lz_size[0] * isle_number:
        above = True
    else:
        above = False

    #Landing detection
    if math.radians(10) >= angle >= math.radians(-10):
        if rocket_pos[1] <= 100 and lz_offset <= rocket_pos[0] <= lz_offset + lz_size[0] * isle_number:
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
    else:
        landed_timer = 3

    #out of map detection
    if now >= 1000 and rocket_pos[0] <= 0 or rocket_pos[0] >= ground.w or rocket_pos[1] >= ceiling:
        out_map = True
    else:
        out_map = False

    #body hit detection
    def coll_begin(arbiter, space, data):
        global boom
        if arbiter.shapes[0].id == 2 and arbiter.shapes[1].id == 0:
            if ground.body._get_velocity()[1]/100 >= 20 or not math.radians(25) >= angle >= math.radians(-25):
                boom = True
        return True

    handler = space.add_default_collision_handler()
    handler.begin = coll_begin

    return landed, landed_timer, boom, out_map, launched, time, above

def restart(rocket_start_pos, ground, rocket, joint1, joint2, rocket_fuel_mass_init, rocket_fuel_mass, screen, landed, gear, last_time, best_time):
    global launched, boom
    keys = pygame.key.get_pressed()
    if keys[K_r]:

        gear = False

        launched = False
        boom = False

        for i in range(1000): #avoid bug
            ground.body.position = (-rocket_start_pos, -50)
            ground.body.velocity = (0, 0)

            rocket.body.angle = 0
            rocket.body.angular_velocity = 0

        joint1.rotary._set_rest_angle(-math.pi/4 * 3)
        joint2.rotary._set_rest_angle(0)

        with open('scores.dat', 'r') as file:
            lines = file.readlines()

            last_time = lines[0]
            best_time = lines[1]


        return rocket_fuel_mass_init, False, gear, launched, last_time, best_time
    return rocket_fuel_mass, landed, gear, launched, last_time, best_time

def score():
    if landed:
        with open('scores.dat', 'r') as file:
            lines = file.readlines()

        lines[0] = str(time) +'\n'

        if float(lines[0]) < float(lines[1]):
            lines[1] = str(time)

        with open('scores.dat', 'w') as file:
            file.writelines(lines)
