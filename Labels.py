import pygame

dt = 1 / 60.0

def text(screen, rocket_body, ground_body, rocket_pos, thrust, gravity, time):
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render('Fuel left: ' + str(rocket_body._get_mass()) + 'kg', 1, (0, 0, 0))
    label_x = myfont.render('x: ' + str(round(rocket_pos[0], 2)), 1, (0, 0, 0))
    label_y = myfont.render('y: ' + str(round(rocket_pos[1], 2)), 1, (0, 0, 0))
    label_TtW = myfont.render('T/W: ' + str(round(thrust/(rocket_body._get_mass()*gravity), 2)), 1, (0, 0, 0))
    label_rocket_speed_x = myfont.render('X Speed: ' + str(round(-ground_body._get_velocity()[0]/10, 0)), 1, (0, 0, 0))
    label_rocket_speed_y = myfont.render('Y Speed: ' + str(round(-ground_body._get_velocity()[1]/10, 0)), 1, (0, 0, 0))
    label_time = myfont.render('t+: {}s'.format(round(time, 1)), 1, (0, 0, 0))


    screen.blit(label, (10, 20))
    screen.blit(label_x, (10, 40))
    screen.blit(label_y, (10, 60))
    screen.blit(label_TtW, (10, 80))
    screen.blit(label_rocket_speed_x, (10, 100))
    screen.blit(label_rocket_speed_y, (10, 120))
    screen.blit(label_time, (10, 140))

    
