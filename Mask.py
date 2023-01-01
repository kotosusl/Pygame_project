import pygame
import math
from load_image import load_image
from pygame.math import Vector2


class Mask(pygame.sprite.Sprite):
    image = load_image('mask2.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Mask.image
        self.x = 500
        self.y = 400
        self.speed = 0.4
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.route = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, args) -> None:
        if args[pygame.K_w]:
            self.x += math.sin(math.radians(self.route)) * self.speed
            self.y -= math.cos(math.radians(self.route)) * self.speed
            self.rect.y = self.y
            self.rect.x = self.x
        elif args[pygame.K_s]:
            self.x -= math.sin(math.radians(self.route)) * self.speed
            self.y += math.cos(math.radians(self.route)) * self.speed
            self.rect.y = self.y
            self.rect.x = self.x
        elif args[pygame.K_a]:
            self.route = (self.route - self.speed) % 360
            self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Mask.image, 360 - self.route)

        elif args[pygame.K_d]:
            self.route = (self.route + self.speed) % 360
            self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Mask.image, 360 - self.route)
