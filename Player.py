import pygame
import math
from load_image import load_image


class Player(pygame.sprite.Sprite):
    image = load_image('player1.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400
        self.route = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args) -> None:
        for event in args:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.route = (self.route + 2) % 360
                    self.image = pygame.transform.rotate(Player.image, self.route)
                if event.key == pygame.K_d:
                    self.route = (self.route - 2) % 360
                    self.image = pygame.transform.rotate(Player.image, self.route)
                if event.key == pygame.K_w:
                    self.rect.x += math.sin(math.radians(self.route)) * 2

