import pygame
from pygame import gfxdraw
import random
import math

'''
Lissajous curves, parametric equations realted to harmonic motion.
Read more at: https://en.wikipedia.org/wiki/Lissajous_curve

Prerequisites: pygame installed
'''

colors_dict = {
"w" : (255, 255, 255),
"r" : (255, 0, 0),
"g" : (0, 255, 0),
"b" : (0, 0, 255),
"y" : (255, 255, 0)}

def to_base64(a):
    ret_str = ["0", "0"]
    if a > 63:
        rem = a % 64
        ret_str[1] = chr(rem + 48)
        a -= rem
        a //= 64
        ret_str[0] = chr(a + 48)
    else:
        ret_str[1] = chr(a + 48)
    return "".join(ret_str)

def to_base10(s):
    return 64 * (ord(s[0]) - 48) + ord(s[1]) - 48

def get_color(c):
    if c == 'x':
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        return colors_dict[c]

print("A Lissajous curve is a curve desribed by the eqautions: x = sin(at + delta), y = sin(bt).")
have_code = input("Do you have a code to enter? (y/n): ")
if have_code == "y":
    cur_code = input("Enter the code (case-sensitive): ")
    cur_code = cur_code.split("-")
    a = to_base10(cur_code[0])
    b = to_base10(cur_code[1])
    delta_num = to_base10(cur_code[2])
    delta_den = to_base10(cur_code[3])
    delta = math.pi * (delta_num / delta_den)
    clr = cur_code[4]
    cur_code = "-".join(cur_code)

    #print(f"a = {a}, b = {b}, delta = {delta_num}/{delta_den}")

else:
    want_random = input("Do you want to generate a random curve? (y/n): ")
    if want_random == "y":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        delta_num = random.randint(1, 100)
        delta_den = random.randint(1, 100)
        delta = math.pi * (delta_num / delta_den)
        clr = random.choice(["r", "g", "b", "y", "w", "x"])
    else:
        a = int(input("a (0 < a < 4096): "))
        if a == 0:
            a = 5
            b = 3
            delta = math.pi / 2
            clr = "x"
        else:
            b = int(input("b (0 < b < 4096): "))
            delta_num = int(input("delta (enter a fraction of pi, numerator): "))
            delta_den = int(input("delta (enter a fraction of pi, denominator): "))
            delta = math.pi * (delta_num / delta_den)
            clr = "q"
            while clr not in ("r", "g", "b", "y", "w", "x"):
                clr = input("Pick the color: r / g / b / y / w / x (rainbow): ")
            
    cur_code = to_base64(a) + "-" + to_base64(b) + "-" + to_base64(delta_num) + "-" + to_base64(delta_den) + "-" + clr

pygame.init()
font = pygame.font.SysFont("verdana", 18)
clock = pygame.time.Clock()
HEIGHT = 800
WIDTH = int(HEIGHT * 1.6)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lissajous Curves")


text = font.render(f"Up/Down arrow to change the speed", True, colors_dict["w"])
WIN.blit(text, (5, HEIGHT - 25))
text = font.render(f"Code: {cur_code}", True, colors_dict["w"])
WIN.blit(text, (5, 5))


def mainloop(win, a, b, A, B, d):
    speed = 64
    t = 0
    run = True
    while run:
        t += 0.01
        x = A * math.sin(a * t + d)
        y = B * math.sin(b * t)
        gfxdraw.filled_circle(win, int(x + WIDTH//2), int(y + HEIGHT//2), 2, get_color(clr))
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
                    if event.key == pygame.K_c:
                        pass
        #print(speed)
        pygame.display.update()
        clock.tick(speed)

mainloop(WIN, a, b, 250, 250, delta)
