import pygame
from befor_init import STATE_MACHINE
from load_image import load_image


def new_mask(mask_number):
    costume = load_image(f'background\\mask{mask_number}.jpg', (0, 0, 0))
    costume = pygame.transform.scale(costume, (1000, 800))
    return costume


class BackgroundMask(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.mask_number = 1
        self.image = new_mask(self.mask_number)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def change_costume(self, fon):
        self.mask_number = fon
        self.image = new_mask(self.mask_number)
        self.mask = pygame.mask.from_surface(self.image)