import pygame
import math
from befor_init import spawn_enemies_x, spawn_enemies_y, size
from load_image import load_image
from random import randint

VIRUS_STATE_MACHINE = 0


class Virus(pygame.sprite.Sprite):
    images = [load_image('virus_red_animation.png', (0, 0, 0)),
              load_image('virus_yellow_animation.png', (0, 0, 0)),
              load_image('virus_blue_animation.png', (0, 0, 0)),
              load_image('virus_red_animation2.png', (0, 0, 0)),
              load_image('virus_yellow_animation2.png', (0, 0, 0)),
              load_image('virus_blue_animation2.png', (0, 0, 0)),
              load_image('virus_red_animation3.png', (0, 0, 0)),
              load_image('virus_yellow_animation3.png', (0, 0, 0)),
              load_image('virus_blue_animation3.png', (0, 0, 0))]

    def __init__(self, virus_enemy_type, fon_number, player_mask, bg_mask, *group):
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

        self.frames1 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1]], 6, 1)
        self.frames2 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1] + 3], 4, 1)
        self.frames3 = self.cut_sheet(Virus.images[virus_enemy_type[fon_number - 1] + 6], 2, 1)
        self.cur_frame = randint(1, 5)
        self.image = self.frames1[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.i = 0

    def cut_sheet(self, sheet, columns, rows):
        lst = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                lst.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return lst

    def update(self, args) -> None:
        self.i += 1
        distance = math.sqrt(((self.x - self.player_mask.x) ** 2) + ((self.y - self.player_mask.y) ** 2))
        if distance > 300:
            VIRUS_STATE_MACHINE = 0
            if self.i > 100:

                self.cur_frame = (self.cur_frame + 1) % len(self.frames1)
                self.image = self.frames1[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.speed = 0.05
            self.x += math.sin(math.radians(self.route)) * self.speed
            self.y += math.cos(math.radians(self.route)) * self.speed
            self.route = (self.route + randint(-6, 6)) % 360
            if self.x < 0 or self.y < 0 or self.x + self.rect[2] > size[0] or self.y + self.rect[3] > size[1]:
                self.x -= math.sin(math.radians(self.route)) * self.speed
                self.y -= math.cos(math.radians(self.route)) * self.speed
                self.route = (self.route + randint(130, 230)) % 360
            if self.iscollide(self.bg_mask):
                self.x -= math.sin(math.radians(self.route)) * self.speed
                self.y -= math.cos(math.radians(self.route)) * self.speed
                self.route = (self.route + randint(100, 260)) % 360
            self.rect.y = self.y
            self.rect.x = self.x

        elif distance < 301 and not self.iscollide(self.player_mask):
            VIRUS_STATE_MACHINE = 0
            if self.i > 120:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
                self.image = self.frames2[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.x += (self.player_mask.x - self.x) * self.speed / 500
            self.y += (self.player_mask.y - self.y) * self.speed / 500

            if self.iscollide(self.bg_mask):
                self.x -= (self.player_mask.x - self.x) * self.speed / 500 - 0.1
                self.y -= (self.player_mask.y - self.y) * self.speed / 500 - 0.1
                self.speed = 0.05
            else:
                if self.speed < self.player_mask.speed + 0.05:
                    self.speed += 0.05
            self.rect.y = self.y
            self.rect.x = self.x
        else:
            if self.i > 140:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames3)
                self.image = self.frames3[self.cur_frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.i = 0
            self.speed = 0.05

    def iscollide(self, mask):
        if pygame.sprite.collide_mask(self, mask):
            VIRUS_STATE_MACHINE = 1
            return True
        return False

