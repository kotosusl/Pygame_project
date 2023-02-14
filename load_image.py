import sys
import pygame
import os


def load_image(name, colorkey=None):  # функция обработки картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):  # обработка отсутствия картинки
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:  # замена выбранного цвета на прозрачный
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image