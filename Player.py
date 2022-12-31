import pygame
from load_image import load_image


class Player(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('player1.png', -1)
        #self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400
        #self.mask = pygame.mask.from_surface(self.image)

