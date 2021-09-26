import pygame
import random
import math

'''
Buffons Needle, a probability experiment that lets us calculate Pi.
Read more at: https://en.wikipedia.org/wiki/Buffon%27s_needle_problem

Prerequisites: pygame installed
'''

pygame.init()
font = pygame.font.SysFont("verdana", 18)
clock = pygame.time.Clock()
HEIGHT = 800
WIDTH = int(HEIGHT * 1.6)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buffons Needle")

cnt = 0
throws = 0
crossed = 0
p = 0
L = 128 
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (175, 216, 245)
YELLOW = (255, 239, 213)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def crosses(x1, x2):
    if (x1 // 256 != x2 // 256) or (x1 == x2 and x1 % 256 == 0):
        return True
    return False

def get_end_pos(x, y):
    base = random.randint(1, 1000000) / 1000000.0
    base *= 359
    angle = math.radians(base)
    return (x + L*math.cos(angle), y + L*math.sin(angle))

def throw(win, on):
    global throws, crossed, p
    for i in range(2):
        pygame.draw.rect(win, GRAY, (i * 512 + 256, 0, 256, HEIGHT))
    for i in range(3):
        pygame.draw.rect(win, WHITE, (i*2*256, 0, 256, HEIGHT))
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    end = get_end_pos(x, y)
    if on:
        pygame.draw.aaline(win, RED, (x, y), end)
    throws += 1
    if (crosses(x, end[0])):
        crossed += 1

    if crossed != 0:
        p = throws / crossed
        #print(p)
    #print(f"begin: {(x, y)}, end: {get_end_pos(x, y)}")
    font = pygame.font.SysFont("verdana", 18)
    text = font.render(f"Pi = {throws} / {crossed} = {round(p, 5)}", True, (0, 0, 0))
    win.blit(text, (0, 0))
    text = font.render(f"Thrown = {throws}", True, (0, 0, 0))
    win.blit(text, (0, 25))
    text = font.render(f"Crossed = {crossed}", True, (0, 0, 0))
    win.blit(text, (0, 50))
    font = pygame.font.SysFont("verdana", 12)
    text = font.render(f"'X' to show or hide the needles | Up/Down arrow to change the speed", True, (0, 0, 0))
    win.blit(text, (5, 780))
    pygame.display.update()

def mainloop(win):
    speed = 1
    flag = 1
    run = True
    while run:
        throw(win, flag)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if speed > 1:
                            speed //= 2
                    if event.key == pygame.K_UP:
                        if speed < 4096:
                            speed *= 2
                    if event.key == pygame.K_x:
                        flag ^= 1
        #print(speed)
        clock.tick(speed)
        
mainloop(WIN)
