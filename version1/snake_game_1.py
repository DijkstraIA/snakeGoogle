from pygame import display, time, draw, QUIT, init, KEYDOWN, K_LEFT, K_DOWN, K_RIGHT, K_UP
from random import randint
import pygame
from numpy import sqrt
import numpy as np


import mss
import cv2
import numpy as np
#from time import time, sleep
import pyautogui

# Variables
#Resolution
w, h = pyautogui.size()

#Input
ini = "s"
end = "q"

#Calculo casilla
eps = 10
disSquard = 40
iniX = 12
iniY = 10

X = 13
Y = 8

wapple = 20
happle = 20 

print("PIL Screen Capture Speed Test")
print("Screen Resolution: " + str(w) + 'x' + str(h))

pyautogui.PAUSE = 0
dim_board = {
        'left': 35,
        'top': 212,
        'width': 680,
        'height': 610
    }

dim_apple = {
        'left': 527, #515,
        'top': 505, #483,
        'width': wapple,
        'height': happle
    }

sct = mss.mss()
apple =  np.array(sct.grab(monitor=dim_apple))
def scan(a,b):
    X = a
    Y = b
    board =  sct.grab(monitor=dim_board)
    board = np.array(board)        
        #Procesar
    result = cv2.matchTemplate(board, apple, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > .75:
        x1 = np.round(((max_loc[0])-iniX)/disSquard + 1)
        y1 = np.round(((max_loc[1])-iniY)/disSquard + 1)
            # print(["x1 ",x1,y1])
            # print(["x2 ", x2,y2])
        # if x1 == x2 and y1 == y2:
        X = x1
        Y = y1
                # print([int(Y),int(X)])
    return int(Y),int(X)


init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

score = 0

cols = 17
rows = 15
iniI = 8
iniJ = 5
posAppleInI = 8
posAppleInJ = 13

width = 408
height = 360
wr = width/cols
hr = height/rows
direction = 1

x = 1200
y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()


def getpath(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        current1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        if current1 == food1:
            break
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False

    def show(self, color):
        draw.rect(screen, color, [self.y*wr+2, self.x*hr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

lenSanke = 4
snake = []

for k in reversed(range(lenSanke)):
    snake.append(grid[iniI-1][iniJ-1-k])

Y,X = scan(posAppleInI,posAppleInJ)
food = grid[Y-1][X-1]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]

it = 0
while not done:
    it+=1
    clock.tick(6.7) #Velocidad de juego
    #time.delay(50)
    screen.fill(BLACK)
    direction = dir_array.pop(-1)
    if direction == 0:    # down
        pyautogui.press("right")
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        pyautogui.press("down")
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        pyautogui.press("left")
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        pyautogui.press("up")
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]
    #Si "come" la manzana
    if current.x == food.x and current.y == food.y:
        score += 1
        cnt = 0
        while 1:
            Y,X = scan(food.x,food.y)
            food = grid[Y-1][X-1]
            cnt+=1
            if not (food in snake):
                break
        print(cnt)
        food_array.append(food)
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)
    # OBSTACULOS 
    for i in range(rows):
        for j in range(cols):
            grid[i][j].show(WHITE)
    
    for spot in snake:
        spot.show(RED)
        

    food.show(GREEN)
    snake[-1].show(BLUE)
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        # elif event.type == KEYDOWN:
        #     if event.key == K_UP and not direction == 0:
        #         direction = 2
        #     elif event.key == K_LEFT and not direction == 1:
        #         direction = 3
        #     elif event.key == K_DOWN and not direction == 2:
        #         direction = 0
        #     elif event.key == K_RIGHT and not direction == 3:
        #         direction = 1