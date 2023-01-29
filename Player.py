import pygame
from load_image import load_image


class Player(pygame.sprite.Sprite):
    image = load_image('player2.png', -1)

    def __init__(self, stmc, player_mask, *group):
        super().__init__(*group)
        self.image = Player.image
        self.player_mask = player_mask
        self.rect = self.player_mask.image.get_rect()
        self.rect.x = self.player_mask.rect.x
        self.rect.y = self.player_mask.rect.y
        self.rect.center = self.player_mask.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        self.st = stmc

    def update(self, *args) -> None:
        self.rect = self.image.get_rect()
        self.rect.x = self.player_mask.rect.x
        self.rect.y = self.player_mask.rect.y
        self.rect.center = self.player_mask.rect.center
        self.route = self.player_mask.route
        self.image = pygame.transform.rotate(Player.image, 360 - self.route)
        #self.mask = pygame.mask.from_surface(self.image)
        if self.st == 6:
            print(6)



