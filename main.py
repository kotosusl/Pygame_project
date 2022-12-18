import pygame
from load_image import load_image
from Player import Player


if __name__ == '__main__':
    pygame.init()
    fon_map = pygame.image.load('pygame fon.png')
    fon_map1 = pygame.transform.scale(fon_map, (2300, 2000))
    pygame.display.set_caption('Anticoronavirus')
    running = True
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon_map1, (0, 0))
        pygame.display.flip()
    pygame.quit()
