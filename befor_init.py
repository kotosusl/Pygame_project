import pygame
from random import randint

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
STATE_MACHINE = 0
virus_amount_of_enemies = [randint(1, 2) for _ in range(9)]
virus_enemy_type = [randint(0, 2) for _ in range(9)]
virus_amount_of_enemies[4] = 3
spawn_enemies_x = [804, 160, 356, 826, 198, 724, 600, 180, 164, 780, 230, 678, 226, 716, 192, 750, 144, 566]
spawn_enemies_y = [254, 522, 420, 580, 284, 586, 388, 688, 324, 414, 272, 600, 288, 562, 524, 582, 686, 324]
