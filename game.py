import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('P-shooter')

clock = pygame.time.Clock()
FPS = 60

x = 200
y = 200

img = pygame.image.load('images/Idle.png')
rect = img.get_rect()
rect.center = (x, y)

running = True

while running:
    dt = clock.tick(FPS) / 1000.0

    screen.fill((135, 206, 235))
    screen.blit(img, rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
