import pygame
from load_image import load_image
from befor_init import size, screen
from Rating import RatingWindow
from Instruction import InstructionWindow
from ButtonClose import ButtonClose
from Settings import SettingsWindow, buttons_sprites_settings

# 0 - в ожидании ответа пользователя
# 1 - запуск игры
# 2 - вывод правил
# 3 - вывод рейтинга
# 4 - правка настроек
# 5 - выход
START_STATE_MACHINE = 0
buttons_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Group()
windows_sprites = pygame.sprite.Group()
close_button_sprites = pygame.sprite.Group()


class ButtonStart(pygame.sprite.Sprite):
    images = [load_image('button_start.png', -1),
              load_image('button_start_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonStart.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect.w // 2
        self.rect.y = 400

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonStart.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 1
        else:
            self.image = ButtonStart.images[0]


class ButtonExit(pygame.sprite.Sprite):
    images = [load_image('button_exit.png', -1),
              load_image('button_exit_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonExit.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 5 - self.rect.w // 2 + 60
        self.rect.y = 600

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonExit.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 5
        else:
            self.image = ButtonExit.images[0]


class ButtonInstruction(pygame.sprite.Sprite):
    images = [load_image('button_instruction.png', -1),
              load_image('button_instruction_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonInstruction.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 3 - self.rect.w // 2 + 60
        self.rect.y = 500

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonInstruction.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 2
        else:
            self.image = ButtonInstruction.images[0]


class ButtonRating(pygame.sprite.Sprite):
    images = [load_image('button_rating.png', -1),
              load_image('button_rating_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonRating.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 5 - self.rect.w // 2 + 60
        self.rect.y = 500

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonRating.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 3
        else:
            self.image = ButtonRating.images[0]


class ButtonSettings(pygame.sprite.Sprite):
    images = [load_image('button_settings.png', -1),
              load_image('button_settings_dark.png', -1)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonSettings.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 3 - self.rect.w // 2 + 60
        self.rect.y = 600

    def update(self, *args) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = ButtonSettings.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 4
        else:
            self.image = ButtonSettings.images[0]


class StartMenu(pygame.sprite.Sprite):
    image = load_image('start2.jpg')

    def __init__(self, *group):
        super(StartMenu, self).__init__(*group)
        self.image = StartMenu.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        ButtonStart(buttons_sprites)
        ButtonSettings(buttons_sprites)
        ButtonExit(buttons_sprites)
        ButtonRating(buttons_sprites)
        ButtonInstruction(buttons_sprites)

    def update(self) -> None:
        buttons_sprites.draw(self.image)


def print_menu(volume, cut_scene):
    global START_STATE_MACHINE
    START_STATE_MACHINE = 0
    running = True
    StartMenu(menu_sprite)
    print_table = None
    close = None

    while running:
        if START_STATE_MACHINE == 5:
            running = False
        elif START_STATE_MACHINE == 1:
            return volume, cut_scene
        elif START_STATE_MACHINE == 3 and print_table is None:
            print_table = RatingWindow(windows_sprites)
            close = ButtonClose(920, 60, close_button_sprites)
        elif START_STATE_MACHINE == 2 and print_table is None:
            print_table = InstructionWindow(windows_sprites)
            close = ButtonClose(920, 60, close_button_sprites)
        elif START_STATE_MACHINE == 4 and print_table is None:
            print_table = SettingsWindow(volume, cut_scene, windows_sprites)
            close = ButtonClose(920, 60, close_button_sprites)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if START_STATE_MACHINE == 3 or START_STATE_MACHINE == 2:
                        close.state = 1
                    else:
                        running = False

        if close and close.state == 1:
            close.kill()
            close = None
            if START_STATE_MACHINE == 4:
                volume = print_table.VOLUME
                cut_scene = print_table.CUT_SCENE
                for button in buttons_sprites_settings:
                    button.kill()
            print_table.kill()
            print_table = None
            START_STATE_MACHINE = 0

        buttons_sprites.update(*events)
        menu_sprite.draw(screen)
        windows_sprites.update(*events)
        windows_sprites.draw(screen)
        close_button_sprites.update(*events)
        close_button_sprites.draw(screen)
        menu_sprite.update()
        pygame.display.flip()
    pygame.quit()
    exit()

