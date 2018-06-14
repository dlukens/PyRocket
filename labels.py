import pygame

dt = 1 / 60.0

def text(screen, rocket, ground, rocket_pos, thrust, gravity, air_density, rocket_empty_mass, screeny, time, last_time, best_time, above):
    myfont_small = pygame.font.SysFont("monospace", 18)
    myfont = pygame.font.SysFont("monospace", 20)
    myfont_big = pygame.font.SysFont("monospace", 40)


    label_fuel = myfont.render('Fuel left: ' + str(round(rocket.body._get_mass() - rocket_empty_mass)) + 'kg', 2, (0, 0, 0))
    label_time2 = myfont_big.render('Time:', 2, (184, 242, 230))
    label_time = myfont_big.render('Time:+{}s'.format(str(time)[:4]), 2, (0, 0, 0))
    label_alt = myfont.render('Altitude: {}km'.format(str(round(rocket_pos[1]/10000, 2))), 2, (0, 0, 0))
    label_TtW = myfont_small.render('T/W: ' + str(round(thrust/(rocket.body._get_mass()*gravity), 2)), 2, (0, 0, 0))
    label_rocket_speed_x = myfont.render('X Speed: ' + str(round(-ground.body._get_velocity()[0]/100, 0)), 2, (0, 0, 0))
    label_rocket_speed_y = myfont.render('Y Speed: ' + str(round(-ground.body._get_velocity()[1]/100, 0)), 2, (0, 0, 0))
    label_air_density = myfont_small.render('Air density:{}kg/m^3'.format(round(air_density, 4)), 2, (0, 0, 0))

    label_info1 = myfont_small.render('Airspeed', 2, (0, 0, 0))
    label_info2 = myfont_small.render('Heading', 2, (0, 0, 0))

    label_last_time = myfont_small.render('Last:{}s'.format(round(float(last_time), 2)), 2, (0, 0, 0))
    label_best_time = myfont_small.render('Best:{}s'.format(round(float(best_time), 2)), 2, (0, 0, 0))

    label_above = myfont_small.render('You are above the target', 2, (0, 0, 0))


    screen.blit(label_time2, (24, 24))
    screen.blit(label_time, (20, 20))
    screen.blit(label_alt, (20, 60))

    screen.blit(label_rocket_speed_x, (20, 100))
    screen.blit(label_rocket_speed_y, (20, 120))
    screen.blit(label_fuel, (20, 160))


    screen.blit(label_info1, (20, screeny - 20))
    screen.blit(label_info2, (130, screeny - 20))
    screen.blit(label_air_density, (240, screeny - 20))
    screen.blit(label_TtW, (540, screeny - 20))
    screen.blit(label_last_time, (680, screeny - 20))
    screen.blit(label_best_time, (840, screeny - 20))

    if above:
        screen.blit(label_above, (680, 210))
