import pygame, pymunk, math
from pygame.color import *

rocket_h = 44
rocket_w = 5

def begin(space, rocket_mass, screenx, screeny, ground_h, ground_w, rocket_start_pos):
    class bodies():
        def __init__(self, w, h, mass, posx, posy, color, id):
            self.posx = posx
            self.posy = posy

            self.w = w
            self.h = h

            vertices = [(0, 0), (w, 0), (w, h), (0, h)]

            self.inertia = pymunk.moment_for_poly(mass, vertices, (0, 100))

            self.body = pymunk.Body(mass, self.inertia)
            self.body.position = posx, posy
            self.body._set_center_of_gravity([w/2, h/2])

            self.shape = pymunk.Poly(self.body, vertices)
            self.shape._set_friction(0.45)
            self.shape.color = color
            self.shape.id = id

            space.add(self.body, self.shape)

    rocket = bodies(rocket_w*4, rocket_h*4, rocket_mass, screenx/2, ground_h + rocket_h, THECOLORS['blue'], 0)
    leg1 = bodies(5, 42, 10000, rocket.posx - rocket.w/2, rocket.posy - 30 - 25/2, THECOLORS['red'], 1)
    leg2 = bodies(5, 42, 10000, rocket.posx + rocket.w/2, rocket.posy - 30 - 25/2, THECOLORS['pink'], 1)

    ground = bodies(ground_w, ground_h, rocket_mass, -rocket_start_pos + ground_w / 2, 0, THECOLORS['red'], 2)
    ground.body._set_moment(pymunk.inf)


    class joints():
        def __init__(self, leg, pin_coord, rotary_angle0, limit_angle0, limit_angle1):

            self.pin = pymunk.constraint.PivotJoint(rocket.body, leg.body, pin_coord, (leg.w/2, 0))

            self.rotary = pymunk.constraint.DampedRotarySpring(leg.body, rocket.body, rotary_angle0, 9e10, 6e9)
            self.rotary.collide_bodies = False

            self.limit = pymunk.constraint.RotaryLimitJoint(leg.body, rocket.body, limit_angle0,  limit_angle1)

            space.add(self.pin, self.rotary, self.limit)

    joint1 = joints(leg1, (rocket.w/4, 6), 0, -math.pi/4 * 3, 0)
    joint2 = joints(leg2, (rocket.w/4 * 3, 6), 0, 0, math.pi/4 * 3)

    rocket_joint = pymunk.constraint.PivotJoint(rocket.body, space.static_body, (rocket.w /2, rocket.h / 2), (screenx / 2, screeny / 2 - 100))
    space.add(rocket_joint)


    return(rocket, leg1, leg2, ground, joint1, joint2)
