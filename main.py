import pygame
from befor_init import size, screen
from load_image import load_image
from Player import Player
from Mask import Mask
from BackgroundMask import BackgroundMask
from Virus import Virus, VIRUS_STATE_MACHINE
from Bullet import Bullet
from Options import Timer, Health, Vaccine
from random import randint
from StartMenu import print_menu

all_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
viruses_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
virus_amount_of_enemies = [randint(1, 2) for _ in range(9)]
virus_amount_of_enemies[4] = 3
viruses_count = sum(virus_amount_of_enemies)
virus_enemy_type = [randint(0, 2) for _ in range(9)]


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
        Virus(virus_enemy_type, fon_number, player_mask, bg_mask, viruses_sprites, all_sprites)


if __name__ == '__main__':

    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    pygame.display.set_caption('Anticoronavirus')
    pygame.mixer.music.load('sounds/Background.wav')
    pygame.mixer.music.play(-1)

    sound_shooting = pygame.mixer.Sound('sounds/Shooting.wav')
    sound_hit_player = pygame.mixer.Sound('sounds/Oops.wav')
    sound_hit_virus = pygame.mixer.Sound('sounds/Booms.wav')

    volume, cut_scene = 100, True

    while True:

        volume, cut_scene = print_menu(volume, cut_scene)
        all_sprites = pygame.sprite.Group()
        background_sprites = pygame.sprite.Group()
        viruses_sprites = pygame.sprite.Group()
        bullets_sprites = pygame.sprite.Group()
        virus_amount_of_enemies = [randint(1, 2) for _ in range(9)]
        virus_amount_of_enemies[4] = 3
        viruses_count = sum(virus_amount_of_enemies)
        virus_enemy_type = [randint(0, 2) for _ in range(9)]
        fon_number = 1
        fon_map = new_fon(fon_number)
        background_mask = BackgroundMask(all_sprites, background_sprites)
        player_mask = Mask(background_mask, all_sprites)
        player = Player(player_mask, all_sprites)
        new_virus(fon_number, player_mask, background_mask)
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        timer = Timer(all_sprites)
        health = Health(player_mask, all_sprites)
        vaccine = Vaccine(viruses_count, all_sprites)
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Bullet(player_mask, player, bullets_sprites, all_sprites)
                        sound_shooting.play()
                if event.type == MYEVENTTYPE:
                    timer.up()
                    damage = pygame.sprite.spritecollide(player_mask, viruses_sprites, False)
                    if damage:
                        player_mask.healthy -= len(damage)
                        health.up()
                        sound_hit_player.play()

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
            hits = pygame.sprite.groupcollide(viruses_sprites, bullets_sprites, False, True)
            all_sprites.update(keys)
            screen.blit(fon_map, (0, 0))
            all_sprites.draw(screen)
            pygame.display.flip()

