import pygame
from load_image import load_image
from befor_init import size


class Timer(pygame.sprite.Sprite):
    image = load_image('option3_1.png', -1)

    def __init__(self, *group):
        super(Timer, self).__init__(*group)
        self.image = Timer.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect.width // 2
        self.rect.y = 5
        self.count = 119
        self.text = f'{self.count // 60}:{str(self.count % 60).rjust(2, "0")}'
        self.font1 = pygame.font.SysFont('sans serif', 48)
        text1 = self.font1.render(self.text, False, (0, 0, 0))
        self.image.blit(text1, (70, 15))

    def up(self):
        self.count -= 1
        self.image = Timer.image.copy()
        self.text = f'{self.count // 60}:{str(self.count % 60).rjust(2, "0")}'
        text1 = self.font1.render(self.text, False, (0, 0, 0))
        self.image.blit(text1, (70, 15))


class Health(pygame.sprite.Sprite):
    image = load_image('option2_1.png', -1)

    def __init__(self, player, *group):
        super(Health, self).__init__(*group)
        self.image = Health.image.copy()
        self.rect = self.image.get_rect()
        self.rect.y = 5
        self.rect.x = size[0] - self.rect.width - 5
        self.font1 = pygame.font.SysFont('sans serif', 55)
        self.player = player
        self.up()

    def up(self):
        self.image = Health.image.copy()
        self.text = self.font1.render(str(self.player.healthy), False, (0, 0, 0))
        self.image.blit(self.text, (50, 15))


class Vaccine(pygame.sprite.Sprite):
    image = load_image('option1_1.png', -1)

    def __init__(self, all_count, *group):
        super(Vaccine, self).__init__(*group)
        self.image = Vaccine.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5
        self.all_count = all_count
        self.kills = 0

    def up(self, kill_count):
        self.image = Vaccine.image.copy()
        pygame.draw.rect(self.image, pygame.Color(0, 150, 255),
                         (38, 17, (72 // self.all_count) * kill_count, 23), 0)
        self.kills = kill_count
