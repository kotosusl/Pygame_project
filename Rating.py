import pygame
from load_image import load_image
import csv


class RatingWindow(pygame.sprite.Sprite):
    image = load_image('rating_table.png', -1)
    row = load_image('rating_row.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = RatingWindow.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        with open('rating.csv', encoding="utf8") as rating_file:
            reader = csv.DictReader(rating_file, delimiter=';', quotechar='"')
            bests = sorted(reader, key=lambda x: int(x['viruses']), reverse=True)
            y = 150
            font1 = pygame.font.SysFont('sans serif', 42)

            for num, row in enumerate(bests):
                image = RatingWindow.row.copy()
                self.number = font1.render(str(num + 1), False, (3, 3, 3))
                self.date = font1.render(row['date'], False, (3, 3, 3))
                self.time = font1.render(row['time'], False, (3, 3, 3))
                self.viruses = font1.render(row['viruses'], False, (3, 3, 3))
                self.health = font1.render(row['health'], False, (3, 3, 3))

                image.blit(self.number, (22, 10))
                image.blit(self.date, (107, 10))
                image.blit(self.time, (369, 10))
                image.blit(self.viruses, (571, 10))
                image.blit(self.health, (753, 10))

                self.image.blit(image, (65, y))
                y += 49