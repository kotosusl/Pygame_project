import pygame
from sys import exit
from load_image import load_image
from befor_init import size, screen
from Rating import RatingWindow
from Instruction import InstructionWindow
from Buttons import ButtonClose
from Settings import SettingsWindow, buttons_sprites_settings
from Buttons import ButtonStart

# 0 - в ожидании ответа пользователя
# 1 - запуск игры
# 2 - вывод правил
# 3 - вывод рейтинга
# 4 - правка настроек
# 5 - выход
START_STATE_MACHINE = 0  # машина состояний стартового меню
buttons_sprites = pygame.sprite.Group()  # определение групп спрайтов
menu_sprite = pygame.sprite.Group()
windows_sprites = pygame.sprite.Group()
close_button_sprites = pygame.sprite.Group()


class ButtonExit(pygame.sprite.Sprite):
    images = [load_image('button_exit.png', -1),  # картинки спрайта
              load_image('button_exit_dark.png', -1)]

    def __init__(self, *group):  # инициализация спрайта
        super().__init__(*group)
        self.image = ButtonExit.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 5 - self.rect.w // 2 + 60
        self.rect.y = 600

    def update(self, *args) -> None:  # обновление кнопки
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # пересечение кнопки с курсором мыши
            self.image = ButtonExit.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE  # изменение состояния меню при нажатии кнопки
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 5
        else:
            self.image = ButtonExit.images[0]


class ButtonInstruction(pygame.sprite.Sprite):
    images = [load_image('button_instruction.png', -1),  # картинки спрайта
              load_image('button_instruction_dark.png', -1)]

    def __init__(self, *group):  # инициализация спрайта
        super().__init__(*group)
        self.image = ButtonInstruction.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 3 - self.rect.w // 2 + 60
        self.rect.y = 500

    def update(self, *args) -> None:  # обновление кнопки перехода в инструкцию
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # проверка пересечения кнопки с курсором
            self.image = ButtonInstruction.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE  # нажатие на кнопку
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 2
        else:
            self.image = ButtonInstruction.images[0]


class ButtonRating(pygame.sprite.Sprite):
    images = [load_image('button_rating.png', -1),  # картинки спрайта
              load_image('button_rating_dark.png', -1)]

    def __init__(self, *group):  # инициализация спрайта
        super().__init__(*group)
        self.image = ButtonRating.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 5 - self.rect.w // 2 + 60
        self.rect.y = 500

    def update(self, *args) -> None:  # обновление кнопки
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # обработка пересечения кнопки с курсором
            self.image = ButtonRating.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE  # обработка нажатия кнопки
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 3
        else:
            self.image = ButtonRating.images[0]


class ButtonSettings(pygame.sprite.Sprite):
    images = [load_image('button_settings.png', -1),  # картинки спрайта
              load_image('button_settings_dark.png', -1)]

    def __init__(self, *group):  # инициализация спрайта
        super().__init__(*group)
        self.image = ButtonSettings.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 9 * 3 - self.rect.w // 2 + 60
        self.rect.y = 600

    def update(self, *args) -> None:  # обновление кнопки
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # обработка пересечения кнопки с курсором
            self.image = ButtonSettings.images[1]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                global START_STATE_MACHINE  # обработка нажатия на кнопку
                if START_STATE_MACHINE == 0:
                    START_STATE_MACHINE = 4
        else:
            self.image = ButtonSettings.images[0]


class StartMenu(pygame.sprite.Sprite):
    image = load_image('start2.jpg')  # картинка спрайта

    def __init__(self, *group):  # инициализация спрайта
        super(StartMenu, self).__init__(*group)
        self.image = StartMenu.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.button_start = ButtonStart(size[0] // 2, 400, buttons_sprites)
        ButtonSettings(buttons_sprites)  # создание кнопок
        ButtonExit(buttons_sprites)
        ButtonRating(buttons_sprites)
        ButtonInstruction(buttons_sprites)

    def update(self) -> None:  # обновление окна
        buttons_sprites.draw(self.image)
        if self.button_start.state == 1:
            global START_STATE_MACHINE  # начало первого уровня
            START_STATE_MACHINE = 1
            self.button_start.state = 0
            self.button_start.kill()


def print_menu(volume, cut_scene):
    global START_STATE_MACHINE  # запуск стартового меню
    START_STATE_MACHINE = 0
    running = True
    StartMenu(menu_sprite)  # запуск стартового окна
    print_table = None
    close = None

    while running:  # основной цикл
        # проверка по машине состояний
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
        for event in events:  # обработка событий
            if event.type == pygame.QUIT:  # обработка закрытия окна
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if START_STATE_MACHINE == 3 or START_STATE_MACHINE == 2:
                        close.state = 1
                    else:
                        running = False

        if close and close.state == 1:  # обработка закрытия внутреигровых окон
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

        buttons_sprites.update(*events)  # обновление всех объектов
        menu_sprite.draw(screen)
        windows_sprites.update(*events)
        windows_sprites.draw(screen)
        close_button_sprites.update(*events)
        close_button_sprites.draw(screen)
        menu_sprite.update()
        pygame.display.flip()
    pygame.quit()  # выход из игры
    exit()

