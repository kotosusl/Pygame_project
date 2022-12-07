import pygame

if __name__ == '__main__':
    pygame.init()
    img = pygame.image.load('pygame fon.png')
    running = True
    size = 700, 500
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(img, (0, 0))
        pygame.display.flip()
    pygame.quit()
