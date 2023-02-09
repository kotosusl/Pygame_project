import pygame
from load_image import load_image


class ButtonClose(pygame.sprite.Sprite):
    images = [load_image('button_close.png', -1),
              load_image('button_close_dark.png', -1)]

    def __init__(self, x, y, *group):
        super(ButtonClose, self).__init__(*group)
        self.image = ButtonClose.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonClose.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                self.state = 1
        else:
            self.image = ButtonClose.images[0]


class ButtonInMenu(pygame.sprite.Sprite):
    images = [load_image('button_inmenu.png', -1),
              load_image('button_inmenu_dark.png', -1)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = ButtonInMenu.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonInMenu.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                self.state = 1
        else:
            self.image = ButtonInMenu.images[0]


class ButtonStart(pygame.sprite.Sprite):
    images = [load_image('button_start.png', -1),
              load_image('button_start_dark.png', -1)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = ButtonStart.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.w // 2
        self.rect.y = y
        self.state = 0

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonStart.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                self.state = 1
        else:
            self.image = ButtonStart.images[0]