import pygame
from befor_init import STATE_MACHINE, size
from load_image import load_image
import math


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet1.png', (0, 0, 0))

    def __init__(self, player_mask,  *group):
        super(Bullet, self).__init__(*group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.player_mask = player_mask
        self.x = player_mask.x
        self.y = player_mask.y
        self.speed = 1
        self.route = player_mask.route
        self.x += math.sin(math.radians((self.route + 90) % 360)) * self.speed * 20
        self.image = pygame.transform.rotate(Bullet.image, 360 - self.route)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, args) -> None:
        self.x += math.sin(math.radians(self.route)) * self.speed
        self.y -= math.cos(math.radians(self.route)) * self.speed
        self.rect.y = self.y
        self.rect.x = self.x
        if self.x < 0 or self.y < 0 or self.y > size[1] or self.x > size[0]:
            self.kill()

        