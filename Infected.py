import math
import pygame
from load_image import load_image
from random import choice


class Infected(pygame.sprite.Sprite):
    images = [load_image('infected.png', -1),
              load_image('man.png', -1)]

    def __init__(self, player, *group):
        super(Infected, self).__init__(*group)
        self.player = player
        self.image = Infected.images[0].copy()
        self.rect = self.image.get_rect()
        self.x = choice([0, 900])
        self.y = choice([0, 700])
        if self.x == 0 and self.y == 0:
            self.route = 40
        elif self.x == 900 and self.y == 0:
            self.route = 140
        elif self.x == 0 and self.y == 700:
            self.route = 320
        elif self.x == 900 and self.y == 700:
            self.route = 220
        self.image = pygame.transform.rotate(Infected.images[0].copy(), 360 - self.route)
        self.mask = pygame.mask.from_surface(self.image)
        self.state = 0
        self.speed = 0.2

    def update(self, bullets_sprites, *args) -> None:
        self.x += math.sin(math.radians((self.route + 90) % 360)) * self.speed
        self.y -= math.cos(math.radians((self.route + 90) % 360)) * self.speed
        if pygame.sprite.collide_mask(self, self.player):
            self.x -= math.sin(math.radians((self.route + 90) % 360)) * self.speed
            self.y += math.cos(math.radians((self.route + 90) % 360)) * self.speed
        self.rect.x = self.x
        self.rect.y = self.y

        if self.state == 0:
            hit = pygame.sprite.spritecollide(self, bullets_sprites, True)
            if hit:
                self.route = (self.route + 180) % 360
                self.image = pygame.transform.rotate(Infected.images[1].copy(), 360 - self.route)
                self.x += math.sin(math.radians((self.route + 90) % 360)) * self.speed
                self.y -= math.cos(math.radians((self.route + 90) % 360)) * self.speed
                self.state = 1
