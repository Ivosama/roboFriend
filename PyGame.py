import pygame
import math
import sys

black = (0, 0, 0)
green = (0, 128, 0)
pygame.init()
screen = pygame.display.set_mode((480, 320))
clock = pygame.time.Clock()
screen.fill(black)
r = math.pi  # Getting the pi value so I don't have to write math.pi every time


def sadFace():
    lEye = pygame.Rect(90, 60, 100, 60)
    rEye = pygame.Rect(270, 60, 100, 60)
    for i in range(12):
        pygame.draw.rect(screen, green, lEye)
        pygame.draw.rect(screen, green, rEye)
        lEye.inflate_ip(i, -i)
        rEye.inflate_ip(i, -i)
    f = 0.1    # This iterates in the next while to get the animation effect
    while f <= r/2:
        clock.tick(300)
        pygame.draw.arc(screen, green, ((60, 200), (350, 90)), r/2 - f, r/2 + f, 10)
        f += 0.01
        pygame.display.update()



def happyFace():
    lEye = pygame.Rect(90, 60, 100, 60)
    rEye = pygame.Rect(270, 60, 100, 60)

    for i in range(10):
        pygame.draw.rect(screen, green, lEye)
        pygame.draw.rect(screen, green, rEye)
        lEye.inflate_ip(-i-3, i+3)
        rEye.inflate_ip(-i-3, i+3)
    f = 0.1  # This iterates in the next while to get the animation effect
    while f < r/2:
        clock.tick(300)
        pygame.draw.arc(screen, green, ((60, 200), (350, 90)), 3*r/2 - f, 3*r/2 + f, 10)
        f += 0.01
        pygame.display.update()


def neutralFace():
    lEye = pygame.Rect(90, 60, 100, 60)
    rEye = pygame.Rect(270, 60, 100, 60)
    for i in range(10):         # Works for some reason
        pygame.draw.rect(screen, green, lEye)
        pygame.draw.rect(screen, green, rEye)
        lEye.inflate_ip(-i, i)
        rEye.inflate_ip(-i, i)
    f = 0   # This iterates in the next while to get the animation effect
    while f <= 145:
        clock.tick(300)
        pygame.draw.line(screen, green, (225-f, 200), (225+f, 200), 10)
        f += 1.7
        pygame.display.update()


while True:    # This needs to loop for the window to stay open
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(black)
    key = pygame.key.get_pressed()       # Something similar should be use in the main code the program is started
    if key[pygame.K_1]:
        happyFace()
    if key[pygame.K_2]:
        sadFace()
    if key[pygame.K_3]:
        neutralFace()
