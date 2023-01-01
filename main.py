import pygame

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()

from load_image import load_image
from Player import Player
from Mask import Mask


def new_fon(fon_number):
    fon_map = load_image(f'map\\fon{fon_number}.jpg')
    fon_map = pygame.transform.scale(fon_map, (1000, 800))
    return fon_map


if __name__ == '__main__':
    pygame.init()
    fon_number = 1
    fon_map = new_fon(fon_number)
    pygame.display.set_caption('Anticoronavirus')
    running = True
    player_mask = Mask(all_sprites)
    player = Player(player_mask, all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if player_mask.x > width and fon_number % 3 != 0:
            fon_number += 1
            fon_map = new_fon(fon_number)
            player_mask.x = 25
        if player_mask.x < 0 and fon_number % 3 != 1:
            fon_number -= 1
            fon_map = new_fon(fon_number)
            player_mask.x = width - 25
        if player_mask.y > height and fon_number < 7:
            fon_number += 3
            fon_map = new_fon(fon_number)
            player_mask.y = 25
        if player_mask.y < 0 and fon_number > 3:
            fon_number -= 3
            fon_map = new_fon(fon_number)
            player_mask.y = height - 25

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        screen.blit(fon_map, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
