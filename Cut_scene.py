import pygame
from load_image import load_image
from befor_init import screen


def play_cut_scene():

    new_viruses = pygame.USEREVENT + 2
    doctor_timer = pygame.USEREVENT + 3
    end_cut_scene = pygame.USEREVENT + 4
    pygame.time.set_timer(doctor_timer, 2000)
    pygame.time.set_timer(new_viruses, 3000)
    pygame.time.set_timer(end_cut_scene, 15000)
    talking = pygame.mixer.Sound('sounds/Talking.wav')
    fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
    viruses = load_image('cut_scene\\viruses0.png', -1)
    doctor = load_image('cut_scene\\doctor1.png', -1)
    fon_image.blit(viruses, (212 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
    doctor_x = 700
    fon_image.blit(doctor, (doctor_x, 500 - doctor.get_rect().h))
    move_doctor = False
    doctor_route = 0
    doctor_x = 700
    talking.play()
    count_images = 1
    doctor_state = 2
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                talking.stop()
                return False
            if event.type == new_viruses:
                pygame.time.set_timer(new_viruses, 1000)
                fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
                viruses = load_image(f'cut_scene\\viruses{count_images}.png')
                fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
                fon_image.blit(doctor, (doctor_x, 500 - doctor.get_rect().h))
                count_images += 1
                if count_images == 8:
                    pygame.time.set_timer(new_viruses, 0)
            if event.type == doctor_timer:
                if doctor_state == 4:
                    doctor = load_image('cut_scene\\doctor2.png', -1)
                    pygame.time.set_timer(doctor_timer, 0)
                    move_doctor = True
                else:
                    doctor = load_image(f'cut_scene\\doctor{doctor_state}.png', -1)
                    if doctor_state == 2:
                        pygame.time.set_timer(doctor_timer, 2500)
                    elif doctor_state == 3:
                        pygame.time.set_timer(doctor_timer, 3000)
                    doctor_state += 1

                fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
                fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
                fon_image.blit(doctor, (doctor_x, 500 - doctor.get_rect().h))
            if event.type == end_cut_scene:
                return True
        if move_doctor:
            if doctor_route != 180:
                doctor_route = (doctor_route + 1) % 360
                doctor = pygame.transform.rotate(load_image('cut_scene\\doctor2.png', -1), doctor_route)
            else:
                doctor_x += 1

            fon_image = pygame.transform.scale(load_image('cut_scene\\fon.png'), (1000, 800))
            fon_image.blit(viruses, (300 - viruses.get_rect().w // 2, 405 - viruses.get_rect().h // 2))
            fon_image.blit(doctor, (doctor_x, 500 - doctor.get_rect().h))
        screen.blit(fon_image, (0, 0))
        pygame.display.flip()



