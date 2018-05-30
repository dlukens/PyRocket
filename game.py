import pygame, pymunk, math

def logic(rocket, ground, rocket_pos, lz_offset, space, angle):

    landed = False

    if math.radians(10) >= angle >= math.radians(-10) and not landed:
        if rocket_pos[1] <= 100 and lz_offset <= rocket_pos[0] <= lz_offset + 20000:
            landed = True

    else:
        landed = False



    def coll_begin(arbiter, space, data):
        if arbiter.shapes[0].id == 2 and  arbiter.shapes[1].id == 0:
            print('boom')

        return True


    handler = space.add_default_collision_handler()

    handler.begin = coll_begin

    return landed
