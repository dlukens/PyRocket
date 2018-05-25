import math, sys, random

import Labels

import numpy as np

import pygame
from pygame.locals import *
from pygame.color import *

try:
    import pymunk
except:
    print("Run pip install pymunk")
    quit()

import pymunk.pygame_util

# ---Set-up---
pygame.init()
screenx = 1000
screeny = 700
screen = pygame.display.set_mode((screenx, screeny))
clock = pygame.time.Clock()
running = True

launch = False

time = 0

# ---Space---
space = pymunk.Space()
# space.gravity = (0.0, -900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

gravity = 900

ceiling = 240000


# ---Ground---

ground_h = 200
ground_w = 800000

ground_img = pygame.image.load('data/grass.jpg').convert_alpha()
ground_img = pygame.transform.scale(ground_img, (200, ground_h))

# ---Rocket---
rocket_fuel_mass = 400000
rocket_empty_mass = 140000

rocket_mass = rocket_empty_mass + rocket_fuel_mass



engine_isp = 330
engine_massflow = 110

thrust = engine_isp * engine_massflow * gravity * 14
force_rcs = 2e7

rocket_h = 44
rocket_w = 5

# ---Bodies---
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

# ---Constraints---
class joints():
    def __init__(self, leg, pin_coord, rotary_angle0, limit_angle0, limit_angle1):

        self.pin = pymunk.constraint.PivotJoint(rocket.body, leg.body, pin_coord, (leg.w/2, 0))

        self.rotary = pymunk.constraint.DampedRotarySpring(leg.body, rocket.body, rotary_angle0, 6e10, 9e8)
        self.rotary.collide_bodies = False

        self.limit = pymunk.constraint.RotaryLimitJoint(leg.body, rocket.body, limit_angle0,  limit_angle1)

        space.add(self.pin, self.rotary, self.limit)

joint1 = joints(leg1, (5, 10), math.pi/4 * 3, -math.pi/4 * 3, 0)
joint2 = joints(leg2, (15, 10), -math.pi/4 * 3, 0, math.pi/4 * 3)

# ---GUI---
def GUI():
    global time
    #minimap
    size = 160
    minimap = pygame.Surface((size, size))
    minimap.set_alpha(120)
    minimap.fill((100,100,100))

    unit_w = size / ground_w
    unit_h = size / ceiling

    minimap_rocket_pos = [0,0]

    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)


    minimap_ground = pygame.draw.rect(minimap, (255,0,0), (0, size - 4, size, 10))

    minimap_rocket = pygame.draw.rect(minimap, (100,150,200), (minimap_rocket_pos[0] + size/2, size - 6 - minimap_rocket_pos[1], 4, 4))

    screen.blit(minimap, (screenx - size - 10, 10))


    dt = 1/60.
    time += dt

    myfont = pygame.font.SysFont("monospace", 20)
    label_time = myfont.render('t+: {}s'.format(round(time,1)), 1, (0, 0, 0))
    screen.blit(label_time, (10, 140))




# ---Main Loop---
while running:
    for event in pygame.event.get():                                            # Exit program
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    if keys[K_w] or launch:
        ground.body.apply_force_at_local_point((thrust*math.sin(angle), -thrust * math.cos(angle)), (rocket.w/2, 0))

        rocket_fuel_mass -= engine_massflow

    if keys[K_d]:
        rocket.body.apply_force_at_local_point((force_rcs, 0), (rocket.w/2, rocket.h))

    if keys[K_a]:
        rocket.body.apply_force_at_local_point((-force_rcs, 0), (rocket.w/2, rocket.h))

    if keys[K_SPACE]:
        launch = True

    # Gravity
    rocket.body.velocity = (0,0)
    angle = pymunk.Body._get_angle(rocket.body)

    if pymunk.Body._get_position(ground.body)[1] < 80:                          #Avoid weird floating
        ground.body.apply_force_at_local_point((0, ground.body._get_mass() * gravity), (0, 0))

    # Miscellaneous
    rocket_mass = rocket_empty_mass + rocket_fuel_mass
    pymunk.Body._set_mass(rocket.body, rocket_mass)
    pymunk.Body._set_mass(ground.body, rocket_mass)

    rocket_pos = -(pymunk.Body._get_position(ground.body)[0] + ground_w/2), -(pymunk.Body._get_position(ground.body)[1] - 30)


    # ---Screen display---
    sky_color_ground = np.array([87, 197, 241])
    sky_color_space = np.array([10, 1, 46])

    sky_color_diff = sky_color_ground - sky_color_space

    color_step = sky_color_diff * (math.exp(rocket_pos[1]*math.log(2)/ceiling) - 1) #function to exponentially change bg color

    bg_color = abs(sky_color_ground - color_step)

    screen.fill(bg_color)

    space.debug_draw(draw_options)

    GUI()

    # ground image
    if rocket_pos[1] < screeny/2:     #prevent weird repeating pattern
        for len in range(0, ground_w, 1400):
            screen.blit(ground_img, pymunk.pygame_util.to_pygame((ground.body._get_position()[0] + len, ground.body._get_position()[1] + ground_h), screen))


    # text
    # Labels.text(rocket.body, ground.body)
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render('Fuel left: ' + str(rocket.body._get_mass()) + 'kg', 1, (0, 0, 0))
    label_x = myfont.render('x: ' + str(round(rocket_pos[0], 2)), 1, (0, 0, 0))
    label_y = myfont.render('y: ' + str(round(rocket_pos[1], 2)), 1, (0, 0, 0))
    label_TtW = myfont.render('T/W: ' + str(round(thrust/(rocket.body._get_mass()*gravity), 2)), 1, (0, 0, 0))
    label_rocket_speed_x = myfont.render('X Speed: ' + str(round(-ground.body._get_velocity()[0]/10, 0)), 1, (0, 0, 0))
    label_rocket_speed_y = myfont.render('Y Speed: ' + str(round(-ground.body._get_velocity()[1]/10, 0)), 1, (0, 0, 0))


    screen.blit(label, (10, 20))
    screen.blit(label_x, (10, 40))
    screen.blit(label_y, (10, 60))
    screen.blit(label_TtW, (10, 80))
    screen.blit(label_rocket_speed_x, (10, 100))
    screen.blit(label_rocket_speed_y, (10, 120))


    # Flip screen
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    # ---Physics---
    dt = 1/60.0
    space.step(dt)

    #TODO camera, payload, thrust logic, gui
