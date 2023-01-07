import pygame
from load_image import load_image
from Player import Player
from Mask import Mask
from BackgroundMask import BackgroundMask
from Virus import Virus
from befor_init import size, screen, STATE_MACHINE, virus_amount_of_enemies
from Bullet import Bullet

all_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
viruses_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()


def new_fon(fon_number):
    fon_map = load_image(f'map\\fon{fon_number}.jpg')
    fon_map = pygame.transform.scale(fon_map, (1000, 800))
    return fon_map


def new_virus(fon_number, player_mask, bg_mask):
    global viruses_sprites
    for i in viruses_sprites:
        i.kill()
    viruses_sprites = pygame.sprite.Group()
    for i in range(virus_amount_of_enemies[fon_number - 1]):
        Virus(fon_number, player_mask, bg_mask, viruses_sprites, all_sprites)



if __name__ == '__main__':
    pygame.init()
    fon_number = 1
    fon_map = new_fon(fon_number)
    pygame.display.set_caption('Anticoronavirus')
    running = True
    background_mask = BackgroundMask(all_sprites, background_sprites)
    player_mask = Mask(background_mask, all_sprites)
    player = Player(player_mask, all_sprites)
    new_virus(fon_number, player_mask, background_mask)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(player_mask, bullets_sprites, all_sprites)
        if fon_number % 3 != 0:
            if player_mask.x > size[0]:
                fon_number += 1
                fon_map = new_fon(fon_number)
                player_mask.x = 25
                background_mask.change_costume(fon_number)
                new_virus(fon_number, player_mask, background_mask)
        else:
            if player_mask.x > size[0] - player_mask.rect[2]:
                player_mask.x = size[0] - player_mask.rect[2]
        if fon_number % 3 != 1:
            if player_mask.x < 0:
                fon_number -= 1
                fon_map = new_fon(fon_number)
                player_mask.x = size[0] - 25
                background_mask.change_costume(fon_number)
                new_virus(fon_number, player_mask, background_mask)
        else:
            if player_mask.x < 0:
                player_mask.x = 0
        if fon_number < 7:
            if player_mask.y > size[1]:
                fon_number += 3
                fon_map = new_fon(fon_number)
                player_mask.y = 25
                background_mask.change_costume(fon_number)
                new_virus(fon_number, player_mask, background_mask)
        else:
            if player_mask.y > size[1] - player_mask.rect[3]:
                player_mask.y = size[1] - player_mask.rect[3]
        if fon_number > 3:
            if player_mask.y < 0:
                fon_number -= 3
                fon_map = new_fon(fon_number)
                player_mask.y = size[1] - 25
                background_mask.change_costume(fon_number)
                new_virus(fon_number, player_mask, background_mask)
        else:
            if player_mask.y < 0:
                player_mask.y = 0


        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        screen.blit(fon_map, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
