from models import Visualisation
import random
from config import *
import pygame
from pygame import \
    (
        QUIT,
        KEYDOWN,
        K_b,
        K_q,
        K_s,
        K_a,
        K_i,
        K_m,
    )

Run = True


def initWindow(width, height):
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("VisualSort")
    return window

def listen2events(V, window):
    global Run
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            Run = False
        if event.type == KEYDOWN:
            if event.key == K_b:
                V.sort()
                V.sortBubble(window)
            if event.key == K_s:
                V.sort()
                V.sortInsertion(window)
            if event.key == K_i:
                V.initArray(ARRAY_SIZE, PADDING, HEIGHT - PADDING)#random.randint(PADDING, HEIGHT - 2 * PADDING))
            if event.key == K_m:
                V.sort()
                V.sortMerge(window)
            if event.key == K_q:
                V.sort()
                V.sortQuick(window)



def main():
    pygame.init()
    Clock = pygame.time.Clock()

    Window = initWindow(WIDTH, HEIGHT)
    V = Visualisation()

    while Run:
        V.draw(Window)
        pygame.display.flip()
        Clock.tick(FPS)
        listen2events(V, Window)

if __name__ == '__main__':
    main()
