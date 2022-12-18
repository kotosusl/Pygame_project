import pygame
from load_image import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('!')
        self.rect.x = self.image.get_rect().x - 50
        self.rect.y = self.image.get_rect().y

