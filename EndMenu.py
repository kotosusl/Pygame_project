import pygame
from load_image import load_image
from befor_init import screen
import datetime
from Buttons import ButtonInMenu
import csv

# 0 - в ожидании ответа
# 1 - выход в меню
END_STATE_MACHINE = 0
buttons_sprites = pygame.sprite.Group()
menu_sprite = pygame.sprite.Group()


class EndMenu(pygame.sprite.Sprite):
    images = [load_image('lose.png'),
              load_image('win.png')]

    def __init__(self, menu_type, *group):
        super().__init__(*group)
        self.image = EndMenu.images[menu_type].copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.button = ButtonInMenu(650, 670, buttons_sprites)

    def update(self) -> None:
        buttons_sprites.draw(self.image)
        if self.button.state == 1:
            global END_STATE_MACHINE
            END_STATE_MACHINE = 1
            self.button.state = 0
            self.button.kill()


def print_end_menu(menu_type, timer, healthy, kills):
    global END_STATE_MACHINE
    END_STATE_MACHINE = 0
    with open('rating.csv', encoding='utf-8') as rating_file_read:
        end_play = {'date': datetime.date.today().strftime('%d.%m.%Y'),
                    'viruses': kills,
                    'time': f'{timer // 60}:{str(timer % 60).rjust(2, "0")}',
                    'health': healthy}
        reader = csv.DictReader(rating_file_read, delimiter=';', quotechar='"')
        top10 = sorted(reader, key=lambda x: int(x['viruses']), reverse=True)[:10]
        top10.append(end_play)
        with open('rating.csv', 'w', newline='', encoding='utf8') as rating_file_write:
            writer = csv.DictWriter(
                rating_file_write, fieldnames=list(top10[0].keys()),
                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(top10)
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
