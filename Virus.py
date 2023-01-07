import pygame
import math
from befor_init import STATE_MACHINE, virus_enemy_type, spawn_enemies_x, spawn_enemies_y, size
from load_image import load_image
from random import randint, random


class Virus(pygame.sprite.Sprite):
    images = [load_image('virus_red.png', (0, 0, 0)),
              load_image('virus_yellow.png', (0, 0, 0)),
              load_image('virus_blue.png', (0, 0, 0))]

    def __init__(self, fon_number, player_mask, bg_mask, *group):
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
        self.route = randint(0, 359)
        self.speed = 0.05
        self.healthy = randint(1, 3)
        self.mask = pygame.mask.from_surface(Virus.images[virus_enemy_type[fon_number - 1]])

    def update(self, args) -> None:
        if self.iscollide(self.bg_mask):
            self.route = (self.route + randint(120, 240)) % 360
            self.image = pygame.transform.rotate(Virus.images[virus_enemy_type[self.fon_number - 1]], 360 - self.route)
            self.x += math.sin(math.radians(self.route)) * self.speed
            self.y += math.cos(math.radians(self.route)) * self.speed
            self.rect.y = self.y
            self.rect.x = self.x
        else:
            distance = math.sqrt(((self.x - self.player_mask.x) ** 2) + ((self.y - self.player_mask.y) ** 2))
            if distance > 330:
                self.x += math.sin(math.radians(self.route)) * self.speed
                self.y += math.cos(math.radians(self.route)) * self.speed
                self.rect.y = self.y
                self.rect.x = self.x
                self.route = (self.route + randint(-6, 6) / 10) % 360
                self.image = pygame.transform.rotate(Virus.images[virus_enemy_type[self.fon_number - 1]],
                                                     360 - self.route)
                if self.x < 0 or self.y < 0 or self.x + self.rect[2] > size[0] or self.y + self.rect[3] > size[1]:
                    self.route = (self.route + 180) % 360
                    self.image = pygame.transform.rotate(Virus.images[virus_enemy_type[self.fon_number - 1]],
                                                         360 - self.route)
            elif distance < 331 and not self.iscollide(self.player_mask):
                rel_x, rel_y = self.player_mask.x - self.x, self.player_mask.y - self.y
                angle = math.atan2(rel_y, rel_x)
                self.route = (math.degrees(angle) + 90) % 360
                self.image = pygame.transform.rotate(Virus.images[virus_enemy_type[self.fon_number - 1]],
                                                     360 - self.route)
                self.x += math.sin(math.radians(self.route)) * self.speed
                self.y += math.cos(math.radians(self.route)) * self.speed
                self.rect.y = self.y
                self.rect.x = self.x
            else:
                self.player_mask.healthy -= 1

    def iscollide(self, mask):
        if pygame.sprite.collide_mask(self, mask):
            return True
        return False

