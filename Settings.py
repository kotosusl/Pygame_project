import pygame
from load_image import load_image


buttons_sprites_settings = pygame.sprite.Group()


class SettingsWindow(pygame.sprite.Sprite):
    image = load_image('settings.png', -1)  # картинка спрайта
    VOLUME = 100
    CUT_SCENE = True

    def __init__(self, volume, cut_scene, *group):  # инициализация окна настроек
        super(SettingsWindow, self).__init__(*group)
        SettingsWindow.VOLUME = volume
        SettingsWindow.CUT_SCENE = cut_scene
        self.image = SettingsWindow.image.copy()
        self.rect = self.image.get_rect()
        Buttons(cut_scene, 'up', 500, 525, buttons_sprites_settings)  # создание кнопок
        Buttons(cut_scene, 'down', 500, 575, buttons_sprites_settings)
        Buttons(cut_scene, 'cut-scene', 500, 325, buttons_sprites_settings)
        self.font = pygame.font.SysFont('sans serif', 50)

    def update(self, *args) -> None:  # обновление окна
        self.image = SettingsWindow.image.copy()
        buttons_sprites_settings.update(*args)  # обновление кнопок
        buttons_sprites_settings.draw(self.image)
        text = self.font.render(f'{SettingsWindow.VOLUME}%', False, (0, 0, 0))
        self.image.blit(text, (600, 550))


class Buttons(pygame.sprite.Sprite):
    images = [load_image('button_up.png', -1),  # картинки спрайта
              load_image('button_up_dark.png', -1),
              load_image('button_down.png', -1),
              load_image('button_down_dark.png', -1),
              load_image('button_cut_scene_true.png', -1),
              load_image('button_cut_scene_false.png', -1)]

    def __init__(self, cut_scene, btn_type, x, y, *group):  # инициализация спрайта
        super(Buttons, self).__init__(*group)
        if btn_type == 'up':  # определение внешнего вида кнопки в зависимости от типа
            self.image = Buttons.images[0]
        elif btn_type == 'down':
            self.image = Buttons.images[2]
        else:
            if cut_scene:
                self.image = Buttons.images[4]
            else:
                self.image = Buttons.images[5]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args) -> None:  # обновление кнопок
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # проверка пересечения с курсором мыши
            if self.image == Buttons.images[0]:
                self.image = Buttons.images[1]
            if self.image == Buttons.images[2]:
                self.image = Buttons.images[3]
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                # проверка нажатия на кнопки
                # регулировка громкости и кат-сцены
                if self.image == Buttons.images[1]:
                    if SettingsWindow.VOLUME + 10 <= 100:
                        SettingsWindow.VOLUME += 10
                        pygame.mixer.music.set_volume(SettingsWindow.VOLUME / 100)
                elif self.image == Buttons.images[3]:
                    if SettingsWindow.VOLUME - 10 >= 0:
                        SettingsWindow.VOLUME -= 10
                        pygame.mixer.music.set_volume(SettingsWindow.VOLUME / 100)
                elif self.image == Buttons.images[4]:
                    SettingsWindow.CUT_SCENE = False
                    self.image = Buttons.images[5]
                elif self.image == Buttons.images[5]:
                    SettingsWindow.CUT_SCENE = True
                    self.image = Buttons.images[4]
        else:
            if self.image == Buttons.images[1]:
                self.image = Buttons.images[0]
            elif self.image == Buttons.images[3]:
                self.image = Buttons.images[2]