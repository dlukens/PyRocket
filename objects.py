import pygame, pymunk, math, random, os
from pygame.color import *

rocket_w = 16
rocket_h = 128

def begin(space, rocket_mass, screenx, screeny, ground_h, ground_w, rocket_start_pos, screen):
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
            self.shape._set_friction(0.5)
            self.shape.color = color
            self.shape.id = id

            space.add(self.body, self.shape)

    rocket = bodies(rocket_w, rocket_h, rocket_mass, screenx/2, ground_h + rocket_h, (120, 120, 120, 255), 0)
    leg1 = bodies(4, 32, 10000, rocket.posx - rocket.w/2, rocket.posy - 30 - 25/2, (80, 80, 80, 255), 1)
    leg2 = bodies(4, 32, 10000, rocket.posx + rocket.w/2, rocket.posy - 30 - 25/2, (80, 80, 80, 255), 1)

    ground = bodies(ground_w, ground_h, rocket_mass, -rocket_start_pos + ground_w / 2, 100, THECOLORS['red'], 2)
    ground.body.position = (-rocket_start_pos, -50)
    ground.body._set_moment(pymunk.inf)


    class joints():
        def __init__(self, leg, pin_coord, rotary_angle0, limit_angle0, limit_angle1):

            self.pin = pymunk.constraint.PivotJoint(rocket.body, leg.body, pin_coord, (leg.w/2, 0))

            self.rotary = pymunk.constraint.DampedRotarySpring(leg.body, rocket.body, rotary_angle0, 8e9, 2e9)
            self.rotary.collide_bodies = False

            self.limit = pymunk.constraint.RotaryLimitJoint(leg.body, rocket.body, limit_angle0,  limit_angle1)

            space.add(self.pin, self.rotary, self.limit)

    joint1 = joints(leg1, (rocket.w/4, 6), 0, -math.pi/4 * 3, 0)
    joint2 = joints(leg2, (rocket.w/4 * 3, 6), 0, 0, math.pi/4 * 3)

    rocket_joint = pymunk.constraint.PivotJoint(rocket.body, space.static_body, (rocket.w /2, rocket.h / 2), (screenx / 2, ground.h + rocket.w/2))
    space.add(rocket_joint)

    class clouds():
        def __init__(self, number):
            layers = [8000, 12000, 20000, 32000, 50000, 120000, 200000, 250000]
            self.number = number

            self.list = []
            self.imglist = []
            load_img_list = []

            self.max_len = 3000
            self.max_he = 1200

            for i in range(len(os.listdir('./data/clouds'))-1):
                cloud_img = pygame.image.load('data/clouds/cloud{}.png'.format(i+1)).convert_alpha()
                load_img_list.append(cloud_img)

            for i in range(4):

                cloud_size = random.randint(1500, self.max_len), random.randint(750, self.max_he)

                self.imglist.append(random.choice(load_img_list))
                self.imglist[i] = pygame.transform.scale(self.imglist[i], cloud_size)

            for i in range(number):
                rand_layer = random.randint(-2200,2200)
                self.list.append((random.randint(0, ground_w), random.choice(layers) + rand_layer))
                self.list[i] = pymunk.pygame_util.to_pygame(self.list[i], screen)

                if len(self.imglist) < number:
                    self.imglist.append(random.choice(self.imglist))


    cloud = clouds(4000)


    return(rocket, ground, joint1, joint2, rocket_joint, cloud)
