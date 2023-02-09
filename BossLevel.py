import pygame
from load_image import load_image
from befor_init import screen
from player_for_boss_level import Player
from ButtonInMenu import ButtonInMenu
from ButtonStart import ButtonStart
from Infected import Infected
from random import randint
from Options import Health, Vaccine
from Bullet import Bullet

# 0 - второй уровень не начат
# 1 - второй уровень начат
# 2 - выход в меню
BOSS_LEVEL_STATE_MACHINE = 0
player_sprite = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()
window_sprite = pygame.sprite.Group()
infected_sprites = pygame.sprite.Group()
options_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()


class Window(pygame.sprite.Sprite):
    image = load_image('to_boss_level.png')

    def __init__(self, *group):
        super(Window, self).__init__(*group)
        self.image = Window.image
        self.rect = self.image.get_rect()
        self.button_in_menu = ButtonInMenu(410, 670, button_sprites)
        self.button_start = ButtonStart(500, 570, button_sprites)

    def update(self, *events) -> None:
        button_sprites.update(*events)
        button_sprites.draw(self.image)
        global BOSS_LEVEL_STATE_MACHINE
        if self.button_in_menu.state == 1:
            BOSS_LEVEL_STATE_MACHINE = 2
            self.button_in_menu.state = 0
            self.button_in_menu.kill()
            self.button_start.kill()
        if self.button_start.state == 1:
            BOSS_LEVEL_STATE_MACHINE = 1
            self.button_start.state = 0
            self.button_start.kill()
            self.button_in_menu.kill()


def boss_level(healthy):
    global BOSS_LEVEL_STATE_MACHINE
    BOSS_LEVEL_STATE_MACHINE = 0
    before_boss_level = Window(window_sprite)
    while BOSS_LEVEL_STATE_MACHINE == 0:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
        before_boss_level.update(*events)
        window_sprite.draw(screen)
        pygame.display.flip()

    if BOSS_LEVEL_STATE_MACHINE == 1:
        fon = pygame.transform.scale(load_image('boss_level_fon.png'), (1000, 800))
        player = Player(healthy, player_sprite)
        spawn_infected = pygame.USEREVENT + 10
        pygame.time.set_timer(spawn_infected, randint(1000, 2000))
        get_damage = pygame.USEREVENT + 9
        pygame.time.set_timer(get_damage, 1000)
        sound_hit_player = pygame.mixer.Sound('sounds/Oops.wav')
        sound_shooting = pygame.mixer.Sound('sounds/Shooting.wav')
        health = Health(player, options_sprites)
        vaccine = Vaccine(11, options_sprites)
        vaccine.up(11)
        count_infected = 0
        end_boss_level = pygame.USEREVENT + 12
        pygame.time.set_timer(end_boss_level, 0)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    player.kill()
                    vaccine.kill()
                    health.kill()
                    for infected in infected_sprites:
                        infected.kill()
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if vaccine.kills != 0:
                            Bullet(1, player, bullets_sprites)
                            sound_shooting.play()
                            vaccine.up(vaccine.kills - 1)
                if event.type == spawn_infected:
                    pygame.time.set_timer(spawn_infected, randint(1000, 2000))
                    Infected(player, infected_sprites)
                    count_infected += 1
                    if count_infected == 10:
                        pygame.time.set_timer(spawn_infected, 0)
                        pygame.time.set_timer(end_boss_level, 2000)
                if event.type == get_damage:
                    damage = pygame.sprite.spritecollide(player, infected_sprites, False)
                    if damage:
                        player.healthy = (player.healthy - len(damage)
                                          if player.healthy - len(damage) >= 0 else 0)
                        health.up()
                        sound_hit_player.play()
                        if player.healthy == 0:
                            player.kill()
                            vaccine.kill()
                            health.kill()
                            for infected in infected_sprites:
                                infected.kill()
                            return False
                if event.type == end_boss_level:
                    player.kill()
                    vaccine.kill()
                    health.kill()
                    for infected in infected_sprites:
                        infected.kill()
                    return True

            keys = pygame.key.get_pressed()
            player_sprite.update(keys)
            screen.blit(fon, (0, 0))
            infected_sprites.update(bullets_sprites, *events)
            bullets_sprites.update(keys)
            infected_sprites.draw(screen)
            player_sprite.draw(screen)
            bullets_sprites.draw(screen)
            options_sprites.draw(screen)
            pygame.display.flip()

    elif BOSS_LEVEL_STATE_MACHINE == 2:
        return 'quit'
