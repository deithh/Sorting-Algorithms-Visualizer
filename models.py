import pygame
from config import *
import sys
import random
import numpy
from pygame.mixer import Sound, get_init, pre_init
from pygame import \
    (
        QUIT,
        KEYDOWN,
        K_ESCAPE,
    )

class Note(Sound):

    def __init__(self, frequency, fps, volume=.1):
        self.frequency = frequency
        self.time = 1/fps
        super().__init__(self.build())
        self.set_volume(volume)

    def build(self):
        lenght = get_init()[0] / self.frequency
        a = 2 ** (abs(get_init()[1]) - 1) - 1
        samples = numpy.array([-a * numpy.sin(-2* numpy.pi * x / lenght) for x in range(int(lenght))])
        samples = numpy.resize(samples, int(get_init()[0]*self.time)).astype(numpy.int16)
        return samples

def hsv2rgb(hue, sat = 1, val = 1):

    c = sat * val
    x = c * (1 - abs((hue/60) % 2 - 1))
    m = val - c
    if 60 > hue:
        rgb = (c,x,0)
    elif 120 > hue:
        rgb = (x,c,0)
    elif 180 > hue:
        rgb = (0,c,x)
    elif 240 > hue:
        rgb = (0,x,c)
    elif 300 > hue:
        rgb = (x,0,c)
    elif 360 > hue:
        rgb = (c,0,x)
    else:
        return -1


    rgb = [int((i+m)*255) for i in rgb]
    return rgb

def work(func):
    def wrapper(self, *args, **kwargs):

        if self.work is False:
            return

        func(self, *args, **kwargs)

    return wrapper

class Visualisation:
    def __init__(self):
        self.work = False
        self.array = []
        self.clock = pygame.time.Clock()
        self.arrayMax = None

    def initArray(self, size, min, max):
        self.array = numpy.linspace(min, max, size)
        random.shuffle(self.array)
        self.arrayMax = max

    def draw(self, window,  comp = -1, comp2 = -1):
        window.fill(BLACK)

        if len(self.array):
            window_width = window.get_width()
            window_height = window.get_height()
            width = window_width // len(self.array)
            fit = (window_width - len(self.array) * width) // 2

            for i, j in enumerate(self.array):
                r, g, b = ARRAY_C

                if MODE == 'color':
                    hue = (j * 230 / self.arrayMax) + 30
                    r, g, b = hsv2rgb(hue, 1, 1)

                if i == comp or i == comp2:
                    # tone = Note(int(self.array[i])+50, uFPS, .1)
                    # tone.play()
                    pygame.draw.rect(window, POINTER_C, (i*width + fit, window_height - j, width, window_height), 0)

                else:
                    pygame.draw.rect(window, (r, g, b), (i*width + fit, window_height - j, width, window_height), 0)

    def update(self, window,  comp = -1, comp2 = -1):
        self.draw(window, comp, comp2)
        pygame.display.flip()
        self.clock.tick(uFPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.work = False

    def sort(self):
        self.work = True

    def shuffle(self):
        random.shuffle(self.array)

    @work
    def sortBubble(self, window):

        for i in range(len(self.array)):

            if not self.work:
                    break
            for j in range(len(self.array)-1 - i):

                if not self.work:
                    break
                if self.array[j+1]<self.array[j]:
                    self.array[j], self.array[j+1]=self.array[j+1],self.array[j]

                self.update(window, j, j+1)

    @work
    def sortSelection(self, window): #in place

        for i in range(len(self.array)):
            min_, min_i = float('inf'), -1
            if not self.work:
                break
            for j in range(i, len(self.array)):
                if not self.work:
                    break
                self.update(window, j, min_i)

                if self.array[j] < min_:
                    min_, min_i = self.array[j], j


            self.array[i], self.array[min_i] = self.array[min_i], self.array[i]
            self.update(window, i, min_i)

    @work
    def sortInsertion(self, window): # in place
        for i in range(len(self.array)+1):
            if not self.work:
                    break
            for j in range(i-1, 0, -1):
                if not self.work:
                    break

                self.update(window, j-1 ,j)

                if self.array[j] < self.array[j-1]:
                    self.array[j], self.array[j-1] = self.array[j-1], self.array[j]
                else:
                    break

    def _partition(self, window, begin, end):
        pivot = random.randint(begin, end)
        self.array[pivot], self.array[end] = self.array[end], self.array[pivot]
        self.update(window, end, pivot)
        pivot = end
        wall = begin
        for index, i in enumerate(self.array[begin:end]):
            if not self.work:
                break
            index += begin
            self.update(window, index, pivot)

            if i < self.array[pivot]:
                self.array[index], self.array[wall] = self.array[wall], self.array[index]
                self.update(window, index, wall)

                wall +=1
        self.array[pivot], self.array[wall] = self.array[wall], self.array[pivot]

        self.update(window, pivot, wall)

        return wall

    @work
    def sortQuick(self, window, begin = 0, end = None):
        if end == None:
            end = len(self.array) - 1
        if begin > end:
            return
        wall = self._partition(window, begin, end)

        self.sortQuick(window, begin, wall - 1)
        self.sortQuick(window, wall + 1, end )

    def _merge(self, window, begin, mid, end):

        L = self.array[begin:mid+1].copy()
        R = self.array[mid+1:end+1].copy()

        i1, i2 = 0, 0

        while i1 < len(L) and i2 < len(R):
            if not self.work:
                break
            if L[i1] < R[i2]:
                self.array[begin + i1 + i2] = L[i1]
                i1+=1
            else:
                self.array[begin + i1 + i2] = R[i2]
                i2+=1

            self.update(window, begin + i1 + i2 -1)


        while i1 < len(L):
            if not self.work:
                break
            self.array[begin + i1 + i2] = L[i1]
            i1+=1
            self.update(window, begin + i1 + i2 -1)
        while i2 < len(R):
            if not self.work:
                break
            self.array[begin + i1 + i2] = R[i2]
            i2+=1
            self.update(window, begin + i1 + i2 -1)

    @work
    def sortMerge(self, window, begin = 0, end = None):
        if end is None:
            end = len(self.array)-1
        if begin >= end:
            return
        mid = (begin + (end - 1))//2
        self.sortMerge(window, begin, mid)
        self.sortMerge(window, mid + 1, end)
        self._merge(window, begin, mid, end)














