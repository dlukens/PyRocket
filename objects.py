import pygame, pymunk, math
from pygame.color import *

def begin(space, rocket_mass, screenx, ground_h, ground_w):

    rocket_h = 44
    rocket_w = 5

    class bodies():
        def __init__(self, w, h, mass, posx, posy, color):
            self.posx = posx
            self.posy = posy

            self.w = w
            self.h = h

            vertices = [(0, 0), (w, 0), (w, h), (0, h)]

            self.inertia = pymunk.moment_for_poly(mass, vertices)

            self.body = pymunk.Body(mass, self.inertia)
            self.body.position = posx, posy
            self.body._set_center_of_gravity([w/2, h/2])

            self.shape = pymunk.Poly(self.body, vertices)
            self.shape._set_friction(0.5)
            self.shape.color = color

            space.add(self.body, self.shape)

    rocket = bodies(rocket_w*4, rocket_h*4, rocket_mass, screenx/2, ground_h + rocket_h, THECOLORS['blue'])
    leg1 = bodies(4, 40, 10000, rocket.posx - rocket.w/2 + 4, rocket.posy - 30 - 25/2, THECOLORS['red'])
    leg2 = bodies(4, 40, 10000, rocket.posx + rocket.w/2 - 4, rocket.posy - 30 - 25/2, THECOLORS['pink'])

    ground = bodies(ground_w, ground_h, rocket_mass, 0, 0, THECOLORS['red'])
    ground.body._set_moment(pymunk.inf)


    class joints():
        def __init__(self, leg, pin_coord, rotary_angle0, limit_angle0, limit_angle1):

            self.pin = pymunk.constraint.PivotJoint(rocket.body, leg.body, pin_coord, (leg.w/2, 0))

            self.rotary = pymunk.constraint.DampedRotarySpring(leg.body, rocket.body, rotary_angle0, 6e10, 9e8)
            self.rotary.collide_bodies = False

            self.limit = pymunk.constraint.RotaryLimitJoint(leg.body, rocket.body, limit_angle0,  limit_angle1)

            space.add(self.pin, self.rotary, self.limit)

    joint1 = joints(leg1, (5, 10), math.pi/4 * 3, -math.pi/4 * 3, 0)
    joint2 = joints(leg2, (15, 10), -math.pi/4 * 3, 0, math.pi/4 * 3)

    return(rocket, leg1, leg2, ground, joint1, joint2)
