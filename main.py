import pygame
from load_image import load_image
from Player import Player


if __name__ == '__main__':
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    fon_map = load_image('map\\fon1.jpg')
    fon_map = pygame.transform.scale(fon_map, (1000, 800))
    pygame.display.set_caption('Anticoronavirus')
    running = True
    Player(all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon_map, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
