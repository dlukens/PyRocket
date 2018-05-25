import pygame

time = 0

def GUI(screen, ground_w, ceiling, screenx, rocket_pos):
    global time
    # minimap
    size = 160
    minimap = pygame.Surface((size, size))
    minimap.set_alpha(120)
    minimap.fill((100, 100, 100))

    unit_w = size / ground_w
    unit_h = size / ceiling

    minimap_rocket_pos = [0, 0]

    minimap_rocket_pos[0] = round(rocket_pos[0] * unit_w, 2)
    minimap_rocket_pos[1] = round(rocket_pos[1] * unit_h, 2)

    minimap_ground = pygame.draw.rect(
        minimap, (255, 0, 0), (0, size - 4, size, 10))

    minimap_rocket = pygame.draw.rect(minimap, (100, 150, 200), (
        minimap_rocket_pos[0] + size / 2, size - 6 - minimap_rocket_pos[1], 4, 4))

    screen.blit(minimap, (screenx - size - 10, 10))

    dt = 1 / 60.
    time += dt

    myfont = pygame.font.SysFont("monospace", 20)
    label_time = myfont.render('t+: {}s'.format(round(time, 1)), 1, (0, 0, 0))
    screen.blit(label_time, (10, 140))
