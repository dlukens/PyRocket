import pygame

dt = 1 / 60.0

def text(screen, rocket, ground, rocket_pos, thrust, gravity, time, air_density):
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render('Fuel left: ' + str(rocket.body._get_mass()) + 'kg', 1, (0, 0, 0))
    label_x = myfont.render('x: {} m'.format(str(round(rocket_pos[0], 2))), 1, (0, 0, 0))
    label_y = myfont.render('y: {} km'.format(str(round(rocket_pos[1]/1000, 2))), 1, (0, 0, 0))
    label_TtW = myfont.render('T/W: ' + str(round(thrust/(rocket.body._get_mass()*gravity), 2)), 1, (0, 0, 0))
    label_rocket_speed_x = myfont.render('X Speed: ' + str(round(-ground.body._get_velocity()[0]/10, 0)), 1, (0, 0, 0))
    label_rocket_speed_y = myfont.render('Y Speed: ' + str(round(-ground.body._get_velocity()[1]/10, 0)), 1, (0, 0, 0))
    label_time = myfont.render('t+: {}s'.format(round(time, 1)), 1, (0, 0, 0))
    label_air_density = myfont.render('Air density: {}kg/m^3'.format(round(air_density, 4)), 1, (0, 0, 0))


    screen.blit(label, (10, 20))
    screen.blit(label_x, (10, 40))
    screen.blit(label_y, (10, 60))
    screen.blit(label_TtW, (10, 80))
    screen.blit(label_rocket_speed_x, (10, 100))
    screen.blit(label_rocket_speed_y, (10, 120))
    screen.blit(label_time, (10, 140))
    screen.blit(label_air_density, (10, 160))
