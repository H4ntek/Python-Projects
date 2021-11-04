import pygame
from pygame import gfxdraw
import math
#import time

pygame.init()
pygame.display.init()
pygame.font.init()

BKG_COLOR = (245, 245, 245)
BIG_FONT = 38
SMALL_FONT = 24
FONT = pygame.font.SysFont("Calibri", 38)
HGT = 800
WDT = int(HGT * 1.6)
WIN = pygame.display.set_mode((WDT, HGT))
NODE_SZ = 30                                  
EPS = 20
MAXN = 100
INF = 100000003

pygame.display.set_caption("Wizualizacja algorytmu DFS - github.com/H4ntek")
WIN.fill(BKG_COLOR)

nodes = [0] * MAXN
nodes_centers = [()] * MAXN
neighbors = [[]] * MAXN
vis = [False] * MAXN

def dist(A, B):
    if not A or not B:
        return INF
    return math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

def check_position(pos):
    for i in range(1, len(nodes_centers)):
        if (dist(nodes_centers[i], pos) < 2 * NODE_SZ + EPS):
            return False
    return True

def clicked_on_node(pos):
    for i in range(1, len(nodes_centers)):
        if (dist(nodes_centers[i], pos) <= NODE_SZ):
            return i
    return -1

def wait_for_space():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

class Node():
    def __init__(self, label, x, y):
        nodes[label] = self
        nodes_centers[label] = (x, y)
        neighbors[label] = []
        self.label = label
        self.x = x
        self.y = y
        self.is_highlighted = False

    def draw(self, color = (0, 0, 0)):
        gfxdraw.filled_circle(WIN, self.x, self.y, NODE_SZ, color)
        gfxdraw.filled_circle(WIN, self.x, self.y, NODE_SZ - 3, (255, 255, 255))
        text = FONT.render(str(self.label), True, (0, 0, 0))
        if len(str(self.label)) == 1:
            WIN.blit(text, (self.x - 9, self.y - 15))
        else:
            WIN.blit(text, (self.x - 19, self.y - 15))

    def connect(self, id):
        if id in neighbors[self.label]:
            return
        neighbors[self.label].append(id)
        neighbors[id].append(self.label)
        print(f"id: {id}, self.label: {self.label}")
        pygame.draw.aaline(WIN, (0, 0, 0), (nodes_centers[id][0], nodes_centers[id][1]), (nodes_centers[self.label][0], nodes_centers[self.label][1]))
        nodes[id].draw()
        nodes[self.label].draw()

    def get_neighbors(self):
        return neighbors[self.label]

    def erase(self, id):
        gfxdraw.filled_circle(WIN, self.x, self.y, NODE_SZ, BKG_COLOR)
        if nodes[id].is_highlighted:
            nodes[id].is_highlighted = False
        for i in range(1, MAXN):
            for j in range(len(neighbors[i])):
                if neighbors[i][j] == id:
                    pygame.draw.line(WIN, BKG_COLOR, (nodes_centers[id][0], nodes_centers[id][1]), (nodes_centers[i][0], nodes_centers[i][1]), 5)
                    nodes[i].draw()
                    neighbors[i][j] = 0
                    break
        neighbors[id].clear()
        nodes[id] = 0
        nodes_centers[id] = ()
    
    def highlight(self, highlighted):
        if not self.is_highlighted:
            self.draw((0, 0, 255))
            self.is_highlighted = True
            highlighted += 1
        else:
            self.draw()
            self.is_highlighted = False
            highlighted -= 1
        return highlighted

def prep_graph():
    run = True
    next_label = 1
    highlighted = 0
    x = 0
    y = 0
    nodes_made = 0

    pygame.draw.aaline(WIN, (0, 0, 0), (0, HGT - 60), (WDT, HGT - 60))
    pygame.draw.aaline(WIN, (0, 0, 0), (WDT - 510, HGT), (WDT - 510, 0))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if nodes_made >= 1:
                        run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                where = clicked_on_node(pos)
                if where != -1:
                    highlighted = nodes[where].highlight(highlighted)
                    if nodes_made >= 2:
                        if highlighted == 2:
                            for i in range(1, next_label):
                                ok = False
                                for j in range(i + 1, next_label):
                                    if nodes[i] != 0 and nodes[j] != 0:
                                        if nodes[i].is_highlighted and nodes[j].is_highlighted:
                                            x = i
                                            y = j
                                            ok = True
                                            break
                                if ok:
                                    break
                            if x != 0 and y != 0:
                                highlighted = nodes[x].highlight(highlighted)
                                highlighted = nodes[y].highlight(highlighted)
                                nodes[x].connect(y)
                                x = 0
                                y = 0


                if check_position(pos):
                    v = Node(next_label, pos[0], pos[1])
                    v.draw()
                    next_label += 1
                    nodes_made += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()

                where = clicked_on_node(pos)
                if where != -1:
                    nodes[where].erase(where)
                    nodes_made -= 1

        pygame.draw.rect(WIN, BKG_COLOR, ((5, HGT - 40), (450, HGT)))
        FONT = pygame.font.SysFont("Calibri", 24)
        text = FONT.render("ENTER - zakończ tworzenie grafu", True, (0, 0, 0))
        FONT = pygame.font.SysFont("Calibri", 38)
        WIN.blit(text, (5, HGT - 40))
        pygame.display.update()

def proper_DFS(v, stack):
    FONT = pygame.font.SysFont("Calibri", 24)
    vis[v] = True
    stack.append(v)

    pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 200, 10), (WDT - 100, HGT - 75)))
    FONT = pygame.font.SysFont("Calibri", BIG_FONT)
    y = 10
    stack = stack[::-1]
    for u in stack:
        text = FONT.render(f"{u}", True, (0, 0, 0))
        WIN.blit(text, (WDT - 200, y))
        y += 40
    stack = stack[::-1]
    FONT = pygame.font.SysFont("Calibri", 24)

    nodes[v].draw((0, 255, 0))
    pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, HGT - 40), (WDT, HGT)))
    text = FONT.render(f"Jestem w wierzchołku {v}", True, (0, 0, 0))
    WIN.blit(text, (WDT - 500, HGT - 40))
    pygame.display.update()
    wait_for_space()
    nodes[v].draw((0, 0, 255))
    pygame.display.update()
    for child in neighbors[v]:
        if not vis[child]:
            pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, HGT - 40), (WDT, HGT)))
            text = FONT.render(f"Wierzchołek {child} jeszcze nie jest odwiedzony, idę tam", True, (0, 0, 0))
            WIN.blit(text, (WDT - 500, HGT - 40))
            pygame.display.update()
            wait_for_space()
            proper_DFS(child, stack)
        else:
            pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, HGT - 40), (WDT, HGT)))
            text = FONT.render(f"Wierzchołek {child} jest już odwiedzony", True, (0, 0, 0))
            WIN.blit(text, (WDT - 500, HGT - 40))
            pygame.display.update()
            wait_for_space()

    stack.pop()
    nodes[v].draw((255, 0, 0))
    pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, HGT - 40), (WDT, HGT)))
    pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 200, 10), (WDT - 100, HGT - 75)))
    FONT = pygame.font.SysFont("Calibri", BIG_FONT)
    y = 10
    stack = stack[::-1]
    for u in stack:
        text = FONT.render(f"{u}", True, (0, 0, 0))
        WIN.blit(text, (WDT - 200, y))
        y += 40
    stack = stack[::-1]
    FONT = pygame.font.SysFont("Calibri", 24)
    text = FONT.render(f"Wszyscy sąsiedzi wierzchołka {v} odwiedzeni", True, (0, 0, 0))
    WIN.blit(text, (WDT - 500, HGT - 40))
    pygame.display.update()
    wait_for_space()


def run_DFS():
    run = True
    end = False
    selected = 0
    FONT = pygame.font.SysFont("Calibri", 24)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                where = clicked_on_node(pos)
                if where != -1:
                    if not selected:
                        selected = where
                        pygame.draw.rect(WIN, BKG_COLOR, ((5, HGT - 40), (500, HGT)))
                        text = FONT.render("SPACJA - wykonaj kolejny krok DFS-a", True, (0, 0, 0))
                        WIN.blit(text, (5, HGT - 40))
                        pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, 10), (WDT - 200, 60)))
                        FONT = pygame.font.SysFont("Calibri", BIG_FONT)
                        text = FONT.render("Stos rekurencji:", True, (0, 0, 0))
                        FONT = pygame.font.SysFont("Calibri", 24)
                        WIN.blit(text, (WDT - 500, 10))
                        pygame.display.update()
                        proper_DFS(where, [])
                        end = True

        if not selected:
            pygame.draw.rect(WIN, BKG_COLOR, ((5, HGT - 40), (500, HGT)))
            text = FONT.render("Wybierz wierzchołek początkowy DFS-a", True, (0, 0, 0))
            WIN.blit(text, (5, HGT - 40))
        if end:
            pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, HGT - 40), (WDT, HGT)))
            pygame.draw.rect(WIN, BKG_COLOR, ((5, HGT - 40), (500, HGT)))
            text = FONT.render("Koniec algorytmu", True, (0, 0, 0))
            WIN.blit(text, (5, HGT - 40))
            pygame.draw.rect(WIN, BKG_COLOR, ((WDT - 500, 10), (WDT - 200, 60)))
        pygame.display.update()

prep_graph()
run_DFS()
