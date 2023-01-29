import pygame
from load_image import load_image
from befor_init import screen

# 0 - в ожидании ответа
# 1 - выход в меню
END_STATE_MACHINE = 0
buttons_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Group()


class ButtonInMenu(pygame.sprite.Sprite):
    images = [load_image('button_inmenu.png', -1),
              load_image('button_inmenu_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonInMenu.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 700

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonInMenu.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global END_STATE_MACHINE
                END_STATE_MACHINE = 1
        else:
            self.image = ButtonInMenu.images[0]


class EndMenu(pygame.sprite.Sprite):
    images = [load_image('lose.png'),
              load_image('win.png')]

    def __init__(self, menu_type, *group):
        super().__init__(*group)
        self.image = EndMenu.images[menu_type].copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        ButtonInMenu(buttons_sprites)

    def update(self) -> None:
        buttons_sprites.draw(self.image)


def print_end_menu(menu_type):
    global END_STATE_MACHINE
    END_STATE_MACHINE = 0

    EndMenu(menu_type, menu_sprite)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                END_STATE_MACHINE = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    END_STATE_MACHINE = 1

        buttons_sprites.update(*events)
        menu_sprite.draw(screen)
        menu_sprite.update()
        pygame.display.flip()
        if END_STATE_MACHINE == 1:
            return
