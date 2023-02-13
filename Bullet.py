import pygame
from befor_init import size
from load_image import load_image
import math


class Bullet(pygame.sprite.Sprite):
    images = [load_image('bullet3.png', (0, 0, 0)),  # картинки спрайта
              load_image('vaccine_bullet.png', -1)]

    def __init__(self, img, player_mask, *group):  # инициализация и появление пули
        super(Bullet, self).__init__(*group)
        self.image = Bullet.images[img]
        self.rect = player_mask.image.get_rect()
        self.x = player_mask.rect.center[0]
        self.y = player_mask.rect.center[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = player_mask.rect.center
        self.speed = 1
        self.route = player_mask.route
        self.image = pygame.transform.rotate(Bullet.images[img], 360 - self.route)
        self.mask = pygame.mask.from_surface(self.image)
        if 200 < self.route < 265:  # калибровка положения относительно игрока
            self.y -= 40
        if 20 < self.route < 70:
            self.y -= 30
        if 160 < self.route < 215:
            self.x -= 20

    def update(self, args) -> None:  # обновление состояния
        self.x += math.sin(math.radians(self.route)) * self.speed  # движение вперёд
        self.y -= math.cos(math.radians(self.route)) * self.speed

        self.rect.y = self.y
        self.rect.x = self.x
        if self.x < 0 or self.y < 0 or self.y > size[1] or self.x > size[0]:
            self.kill()  # самоуничтожение при касании границ локации

        