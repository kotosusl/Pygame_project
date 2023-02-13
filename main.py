import pygame
from befor_init import size, screen
from load_image import load_image
from Player import Player
from Mask import Mask
from BackgroundMask import BackgroundMask
from Virus import Virus, virus_amount_of_enemies, new_init
from Bullet import Bullet
from Options import Timer, Health, Vaccine
from random import randint
from StartMenu import print_menu
from EndMenu import print_end_menu
from Cut_scene import play_cut_scene
from BossLevel import boss_level

# 0 - в игровом меню
# 1 - игра начата и на первом уровне
# 3 - игра выиграна
# 4 - игра проиграна
# 5 - игра на босс-уровне

GLOBAL_STATE_MACHINE = 0  # машина состояний всей игры
all_sprites = pygame.sprite.Group()  # определение групп спрайтов
background_sprites = pygame.sprite.Group()
viruses_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
viruses_count = sum(virus_amount_of_enemies)
virus_enemy_type = [randint(0, 2) for _ in range(9)]


def new_fon(fon_number):  # инициализация нового фона
    fon_map = load_image(f'map\\fon{fon_number}.jpg')
    fon_map = pygame.transform.scale(fon_map, (1000, 800))
    return fon_map


def new_virus(vaccine, fon_number, player_mask, bg_mask):  # появление вирусов, соответствующих фону
    global viruses_sprites, bullets_sprites
    for i in viruses_sprites:
        i.kill()
    viruses_sprites = pygame.sprite.Group()
    for i in range(virus_amount_of_enemies[fon_number - 1]):
        Virus(vaccine, bullets_sprites, virus_enemy_type,
              fon_number, player_mask, bg_mask, viruses_sprites, all_sprites)


if __name__ == '__main__':

    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    pygame.display.set_caption('Anticoronavirus')
    pygame.mixer.music.load('sounds/Background.wav')  # инициализация музыки
    pygame.mixer.music.play(-1)

    sound_shooting = pygame.mixer.Sound('sounds/Shooting.wav')
    sound_hit_player = pygame.mixer.Sound('sounds/Oops.wav')
    sound_hit_virus = pygame.mixer.Sound('sounds/Booms.wav')

    volume, cut_scene = 100, True

    while True:

        GLOBAL_STATE_MACHINE = 0
        volume, cut_scene = print_menu(volume, cut_scene)  # вызов основного меню

        GLOBAL_STATE_MACHINE = 1
        all_sprites = pygame.sprite.Group()  # определение групп спрайтов
        background_sprites = pygame.sprite.Group()
        viruses_sprites = pygame.sprite.Group()
        bullets_sprites = pygame.sprite.Group()

        virus_amount_of_enemies = new_init()  # инициализация первого уровня
        viruses_count = sum(virus_amount_of_enemies)
        virus_enemy_type = [randint(0, 2) for _ in range(9)]
        fon_number = 1
        fon_map = new_fon(fon_number)
        background_mask = BackgroundMask(all_sprites, background_sprites)
        player_mask = Mask(background_mask, all_sprites)
        vaccine = Vaccine(viruses_count, all_sprites)
        player = Player(player_mask, all_sprites)
        new_virus(vaccine, fon_number, player_mask, background_mask)
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        timer = Timer(all_sprites)
        health = Health(player_mask, all_sprites)

        if cut_scene:  # запуск катсцены по необходимости
            pygame.mixer.music.pause()
            print_cut_scene = play_cut_scene()
            pygame.mixer.music.unpause()
            if print_cut_scene:
                running = True
            else:
                running = False
        else:
            running = True

        while running:  # главный игровой цикл первого уровня
            for event in pygame.event.get():  # обработка событий первого уровня
                if event.type == pygame.QUIT:  # обработка закрытия окна
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши
                    if event.button == 1:
                        Bullet(0, player_mask, bullets_sprites, all_sprites)  # стральба
                        sound_shooting.play()
                if event.type == MYEVENTTYPE:  # обновление урона и времени
                    timer.up()
                    if timer.count == 0:
                        GLOBAL_STATE_MACHINE = 4
                    damage = pygame.sprite.spritecollide(player, viruses_sprites, False)
                    if damage:
                        player_mask.healthy = (player_mask.healthy - len(damage)
                                               if player_mask.healthy - len(damage) >= 0 else 0)
                        health.up()
                        sound_hit_player.play()
                        if player_mask.healthy == 0:  # проверка проигрыша
                            GLOBAL_STATE_MACHINE = 4

            if fon_number % 3 != 0:  # переход по локациям
                if player_mask.x > size[0]:
                    fon_number += 1
                    fon_map = new_fon(fon_number)
                    player_mask.x = 25
                    background_mask.change_costume(fon_number)
                    new_virus(vaccine, fon_number, player_mask, background_mask)
                    for bullet in bullets_sprites:
                        bullet.kill()
            else:
                if player_mask.x > size[0] - player_mask.rect[2]:  # столкновение с границей карты
                    player_mask.x = size[0] - player_mask.rect[2]
            if fon_number % 3 != 1:  # переход по локациям
                if player_mask.x < 0:
                    fon_number -= 1
                    fon_map = new_fon(fon_number)
                    player_mask.x = size[0] - 25
                    background_mask.change_costume(fon_number)
                    new_virus(vaccine, fon_number, player_mask, background_mask)
                    for bullet in bullets_sprites:
                        bullet.kill()
            else:
                if player_mask.x < 0:  # столкновение с границей карты
                    player_mask.x = 0
            if fon_number < 7:  # переход по локациям
                if player_mask.y > size[1]:
                    fon_number += 3
                    fon_map = new_fon(fon_number)
                    player_mask.y = 25
                    background_mask.change_costume(fon_number)
                    new_virus(vaccine, fon_number, player_mask, background_mask)
                    for bullet in bullets_sprites:
                        bullet.kill()
            else:
                if player_mask.y > size[1] - player_mask.rect[3]:  # столкновение с границей карты
                    player_mask.y = size[1] - player_mask.rect[3]
            if fon_number > 3:  # переход по локациям
                if player_mask.y < 0:
                    fon_number -= 3
                    fon_map = new_fon(fon_number)
                    player_mask.y = size[1] - 25
                    background_mask.change_costume(fon_number)
                    new_virus(vaccine, fon_number, player_mask, background_mask)
                    for bullet in bullets_sprites:
                        bullet.kill()
            else:
                if player_mask.y < 0:  # столкновение с границей карты
                    player_mask.y = 0

            keys = pygame.key.get_pressed()  # обновление всех объектов уровня
            all_sprites.update(keys)
            screen.blit(fon_map, (0, 0))
            all_sprites.draw(screen)
            pygame.display.flip()

            if sum(virus_amount_of_enemies) == 0:  # проверка победы
                GLOBAL_STATE_MACHINE = 5

            if GLOBAL_STATE_MACHINE == 5:
                play_boss_level = boss_level(player_mask.healthy)  # переход на второй уровень
                if play_boss_level == 'quit':  # обработка победы на втором уровне
                    running = False
                elif play_boss_level is True:
                    GLOBAL_STATE_MACHINE = 3
                else:
                    GLOBAL_STATE_MACHINE = 4

            if GLOBAL_STATE_MACHINE == 3:  # действия при победе
                running = False
                end_menu = print_end_menu(1, timer.count, player_mask.healthy, vaccine.kills)  # вывод конечного меню
                timer.kill()
                vaccine.kill()
                health.kill()
            if GLOBAL_STATE_MACHINE == 4:  # действия при поражении
                running = False
                end_menu = print_end_menu(0, timer.count, player_mask.healthy, vaccine.kills)  # вывод конечного меню
                timer.kill()
                vaccine.kill()
                health.kill()



