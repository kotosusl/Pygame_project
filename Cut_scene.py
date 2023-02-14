import pygame
from load_image import load_image
from befor_init import screen

doctor_sprite = pygame.sprite.Group()


class Doctor(pygame.sprite.Sprite):
    images = [load_image('cut_scene\\doctor1.png', -1),  # картинки спрайта
              load_image('cut_scene\\doctor2.png', -1),
              load_image('cut_scene\\doctor3.png', -1)]

    def __init__(self, *group):  # инициализация спрайта
        super(Doctor, self).__init__(*group)
        self.image = Doctor.images[0]
        self.rect = Doctor.images[1].get_rect()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.route = 0

    def new_image(self, indx):  # смена картинки
        self.image = Doctor.images[indx - 1]

    def update(self, *args) -> None:  # обновление состояния
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image = pygame.transform.rotate(Doctor.images[1], 360 - self.route)


def play_cut_scene():  # инициализация кат-сцены

    new_viruses = pygame.USEREVENT + 2
    doctor_timer = pygame.USEREVENT + 3
    end_cut_scene = pygame.USEREVENT + 4
    pygame.time.set_timer(doctor_timer, 2000)
    pygame.time.set_timer(new_viruses, 3000)
    pygame.time.set_timer(end_cut_scene, 12000)
    talking = pygame.mixer.Sound('sounds/Talking.wav')
    fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
    viruses = load_image('cut_scene\\viruses0.png', -1)
    doctor = Doctor(doctor_sprite)
    fon_image.blit(viruses, (212 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
    doctor.rect.x, doctor.rect.y = 700, 500 - doctor.rect.h
    move_doctor = False
    talking.play()
    count_images = 1
    doctor_state = 2
    while True:  # главный цикл кат-сцены
        events = pygame.event.get()
        for event in events:  # обработка событий
            if event.type == pygame.QUIT:  # обработка закрытия
                talking.stop()
                return False
            if event.type == new_viruses:  # обновление картинки вирусов
                pygame.time.set_timer(new_viruses, 1000)
                fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
                viruses = load_image(f'cut_scene\\viruses{count_images}.png')
                fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
                count_images += 1
                if count_images == 8:
                    pygame.time.set_timer(new_viruses, 0)
            if event.type == doctor_timer:  # обновление картинки доктора
                if doctor_state == 4:
                    doctor.new_image(2)
                    pygame.time.set_timer(doctor_timer, 0)
                    move_doctor = True
                else:
                    doctor.new_image(count_images)
                    if doctor_state == 2:
                        pygame.time.set_timer(doctor_timer, 2500)
                    elif doctor_state == 3:
                        pygame.time.set_timer(doctor_timer, 3000)
                    doctor_state += 1

                fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
                fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
            if event.type == end_cut_scene:  # обработка окончания кат-сцены
                doctor.kill()
                return True
        if move_doctor:  # перемещение доктора
            if doctor.route != 180:
                doctor.route = (doctor.route + 3) % 360
                doctor.rect = doctor.image.get_rect(center=doctor.rect.center)
                doctor.image = pygame.transform.rotate(load_image('cut_scene\\doctor2.png', -1), doctor.route)

            else:
                doctor.rect.x += 3

            fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))  # общее обновление
            fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
        screen.blit(fon_image, (0, 0))
        doctor_sprite.draw(screen)
        pygame.display.flip()



