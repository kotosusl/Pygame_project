import pygame
from load_image import load_image
from befor_init import size


class Player(pygame.sprite.Sprite):
    image = load_image('player2.png', -1)

    def __init__(self, healthy, *group):
        super().__init__(*group)
        self.image = Player.image
        self.healthy = healthy
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect.w // 2
        self.rect.y = size[1] // 2 - self.rect.h // 2
        self.route = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, args) -> None:
        if args[pygame.K_a]:
            self.route = (self.route - 0.5) % 360
            self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Player.image, 360 - self.route)
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(Player.image, 360 - self.route))

        elif args[pygame.K_d]:
            self.route = (self.route + 0.5) % 360
            self.rect = self.image.get_rect(center=self.rect.center)
            self.image = pygame.transform.rotate(Player.image, 360 - self.route)
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(Player.image, 360 - self.route))

