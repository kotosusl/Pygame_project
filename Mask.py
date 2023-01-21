import pygame
import math
from load_image import load_image
from befor_init import STATE_MACHINE


class Mask(pygame.sprite.Sprite):
    image = load_image('mask2.png')

    def __init__(self, bg_mask, *group):
        super().__init__(*group)
        self.image = Mask.image
        self.bg_mask = bg_mask
        self.healthy = 5
        self.x = 500
        self.y = 400
        self.speed = 0.6
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.route = 0
        self.mask = pygame.mask.from_surface(load_image('mask2.png'))

    def update(self, args) -> None:
        if args[pygame.K_w]:
            self.x += math.sin(math.radians(self.route)) * self.speed
            self.y -= math.cos(math.radians(self.route)) * self.speed
            self.rect.y = self.y
            self.rect.x = self.x
            if self.iscollide():
                self.x -= math.sin(math.radians(self.route)) * self.speed
                self.y += math.cos(math.radians(self.route)) * self.speed
                self.rect.y = self.y
                self.rect.x = self.x
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(load_image('mask2.png'), 360 - self.route))

        elif args[pygame.K_s]:
            self.x -= math.sin(math.radians(self.route)) * self.speed / 2
            self.y += math.cos(math.radians(self.route)) * self.speed / 2
            self.rect.y = self.y
            self.rect.x = self.x
            if self.iscollide():
                self.x += math.sin(math.radians(self.route)) * self.speed / 2
                self.y -= math.cos(math.radians(self.route)) * self.speed / 2
                self.rect.y = self.y
                self.rect.x = self.x
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(load_image('mask2.png'), 360 - self.route))

        elif args[pygame.K_a]:
            self.route = (self.route - self.speed) % 360
            #self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Mask.image, 360 - self.route)
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(load_image('mask2.png'), 360 - self.route))

        elif args[pygame.K_d]:
            self.route = (self.route + self.speed) % 360
            #self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Mask.image, 360 - self.route)
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(load_image('mask2.png'), 360 - self.route))

    def iscollide(self):
        if pygame.sprite.collide_mask(self, self.bg_mask):
            return True
        return False