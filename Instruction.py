from load_image import load_image
import pygame


class InstructionWindow(pygame.sprite.Sprite):
    image = load_image('instruction_table.png', -1)

    def __init__(self, *group):
        super(InstructionWindow, self).__init__(*group)
        self.image = InstructionWindow.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

