import pygame
import math
from befor_init import spawn_enemies_x, spawn_enemies_y, size
from load_image import load_image
from random import randint

KILLS_COUNT = 0
virus_amount_of_enemies = [randint(1, 2) for _ in range(9)]
virus_amount_of_enemies[4] = 3


def new_init():  # распределение вирусов на новую игру
    global KILLS_COUNT, virus_amount_of_enemies
    KILLS_COUNT = 0
    virus_amount_of_enemies = [randint(1, 2) for _ in range(9)]
    virus_amount_of_enemies[4] = 3
    return virus_amount_of_enemies


class Virus(pygame.sprite.Sprite):
    images = [load_image('virus_red_animation.png', (0, 0, 0)),  # картинки спрайта
              load_image('virus_yellow_animation.png', (0, 0, 0)),
              load_image('virus_blue_animation.png', (0, 0, 0)),
              load_image('virus_red_animation2.png', (0, 0, 0)),
              load_image('virus_yellow_animation2.png', (0, 0, 0)),
              load_image('virus_blue_animation2.png', (0, 0, 0)),
              load_image('virus_red_animation3.png', (0, 0, 0)),
              load_image('virus_yellow_animation3.png', (0, 0, 0)),
              load_image('virus_blue_animation3.png', (0, 0, 0))]

    def __init__(self, vaccine, bullets_sprites, virus_enemy_type,
                 fon_number, player_mask, bg_mask, *group):  # инициализация спрайта
        super(Virus, self).__init__(*group)
        self.fon_number = fon_number
        self.player_mask = player_mask
        self.bg_mask = bg_mask
        self.image = Virus.images[virus_enemy_type[fon_number - 1]]
        self.rect = self.image.get_rect()
        spawn = randint(fon_number * 2 - 2, fon_number * 2 - 1)
        self.x = spawn_enemies_x[spawn]
        self.y = spawn_enemies_y[spawn]
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = 0.05
        self.route = randint(0, 359)
        self.healthy = randint(1, 3)
        self.clock = pygame.time.Clock()
        self.bullets_sprites = bullets_sprites
        # создание анимации
        self.frames1 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1]], 6, 1)
        self.frames2 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1] + 3], 4, 1)
        self.frames3 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1] + 6], 2, 1)
        self.cur_frame = randint(1, 5)
        self.image = self.frames1[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.i = 0
        self.vaccine = vaccine
        self.sound_hit_virus = pygame.mixer.Sound('sounds/Booms.wav')
        self.sound_hit_virus2 = pygame.mixer.Sound('sounds/Collect.wav')

    def cut_sheet(self, sheet, columns, rows):  # разделение серий картинок с анимацией
        lst = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                lst.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return lst

    def update(self, args) -> None:  # обновление спрайта
        self.i += 1
        # расстояние до игрока
        distance = math.sqrt(((self.x - self.player_mask.x) ** 2) + ((self.y - self.player_mask.y) ** 2))
        if distance > 300:  # если рассояние больше 300 пикселей
            if self.i > 100:

                self.cur_frame = (self.cur_frame + 1) % len(self.frames1)  # переключение анимации
                self.image = self.frames1[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.speed = 0.05
            self.x += math.sin(math.radians(self.route)) * self.speed  # движение вперед
            self.y += math.cos(math.radians(self.route)) * self.speed
            self.route = (self.route + randint(-6, 6)) % 360  # поворот на рандомный угол
            if self.x < 0 or self.y < 0 or self.x + self.rect[2] > size[0] or self.y + self.rect[3] > size[1]:
                self.x -= math.sin(math.radians(self.route)) * self.speed  # отталкивание от границ локации
                self.y -= math.cos(math.radians(self.route)) * self.speed
                self.route = (self.route + randint(130, 230)) % 360
            if self.iscollide(self.bg_mask):
                self.x -= math.sin(math.radians(self.route)) * self.speed  # отталкивание от объектов фона
                self.y -= math.cos(math.radians(self.route)) * self.speed
                self.route = (self.route + randint(100, 260)) % 360
            self.rect.y = self.y
            self.rect.x = self.x

        elif distance < 301 and not self.iscollide(self.player_mask):  # погоня за игроком
            if self.i > 120:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames2)  # переключение анимации
                self.image = self.frames2[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.x += (self.player_mask.x - self.x) * self.speed / 500  # движение в сторону игрока
            self.y += (self.player_mask.y - self.y) * self.speed / 500

            if self.iscollide(self.bg_mask):
                self.x -= (self.player_mask.x - self.x) * self.speed / 500 - 0.1  # отталкивание от объектов фона
                self.y -= (self.player_mask.y - self.y) * self.speed / 500 - 0.1
                self.speed = 0.05
            else:
                if self.speed < self.player_mask.speed + 0.05:
                    self.speed += 0.05
            self.rect.y = self.y
            self.rect.x = self.x
        else:  # при касании игрока
            if self.i > 140:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames3)  # переключение анимации
                self.image = self.frames3[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.speed = 0.05

        self.virus_hits = pygame.sprite.spritecollide(self, self.bullets_sprites, True)
        self.healthy -= len(self.virus_hits)  # получение урона вирусом
        if self.healthy <= 0:
            global KILLS_COUNT  # гибель вируса
            KILLS_COUNT += 1
            self.sound_hit_virus.play()
            self.vaccine.up(KILLS_COUNT)
            virus_amount_of_enemies[self.fon_number - 1] -= 1
            self.kill()
        elif self.virus_hits:
            self.sound_hit_virus2.play()

    def iscollide(self, mask):  # проверка пересечения с заданной маской
        if pygame.sprite.collide_mask(self, mask):
            return True
        return False

