import sys
from pygame import display, time, init
from time import sleep
import time as time2
import pyautogui
import keyboard
import os

from agent.algorithm import algorithms
from model.piece import node
from screen.capture import capture, monitorObj

# [board, apple]
left = [35, 527]
top = [217, 505]
width = [680, 20]
height = [600, 20]

# Tamaño de la casilla en pixeles
wi = 40
hi = 40

#Limite de desincronizacion
lim = 2

#Variables auxiliares
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
dword = ['right', 'down', 'left', 'up']
# dword = ['d', 's', 'a', 'w']

class IA:
    def __init__(self):
        # Variables de captura de pantalla
        board = monitorObj(left[0], top[0], width[0], height[0])
        self.captureImg = capture(board, wi, hi)

        # Instancia del algoritmo
        self.calculate = algorithms()
        init()

        # Variables de juego
        self.score = 0
        self.rows = 15
        self.cols = 17
        
        # Creacion de la reticula
        self.grid = [[node(i, j) for j in range(self.cols)]
                     for i in range(self.rows)]

        # Creacion del grafo
        self.createGraph()

        # Creacion de la serpiente
        self.lenSanke = 4
        headSnake = self.grid[8][5]
        self.snake = self.createSnake(headSnake.x, headSnake.y, self.lenSanke) # La cabeza es el ultimo elemento
        self.headV1 = self.snake[-1]
        self.headV2 = self.snake[-2]
        self.headR1 = self.snake[-1]
        self.headR2 = self.snake[-2]

        # Posicion inicial de la manzana
        self.food = self.grid[8-1][13-1]
        self.searchApple()


    def createGraph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].add_neighbors(self.grid, self.rows, self.cols)

    def createSnake(self, iniI, iniJ, lenSanke):
        snake = []
        for k in reversed(range(lenSanke)):
            snake.append(self.grid[iniI-1][iniJ-1-k])
        return snake

    def play(self):
        sleep(1)
        path = []
        dir_array = [0,0,0,0,0,0,0,0,0]
        try:            
            while 1: #Time max 0.2 por iteracion
                self.searchHead()  ## Sensores
                
                # Si la cabeza real y la virtual son iguales se calcula el siguiente movimiento
                if (abs(self.headV1.x - self.headR1.x) == 0 and abs(self.headV1.y - self.headR1.y) == 0) or  (abs(self.headV2.x - self.headR2.x) == 0 and abs(self.headV2.y - self.headR2.y) == 0):
                    direction = dir_array.pop(-1)
                    path = self.move(self.headV1, direction, path)
                    dir = path.pop(0)
                    
                    self.moveSnake(dir)  ## Actuadores
                    
                    if self.headV1.x == self.food.x and self.headV1.y == self.food.y:
                        self.score += 1
                        self.searchApple()  ## Sensores
                        
                        ## Algoritmos ## Funcion interna de calculo
                        dir_array = self.calculate.asterisk2(self.food, self.snake, self.rows, self.cols)
                        # dir_array = self.calculate.asterisk1(self.food, self.snake, self.grid, self.rows, self.cols)
                        # dir_array = self.calculate.bfs(self.food, self.snake, self.rows, self.cols)
                        # dir_array = self.calculate.dfsAll(self.food, self.snake, self.rows, self.cols)

                    else:
                        self.snake.pop(0)
                        
                if keyboard.is_pressed("q") or self.endGame():
                    break
            print(["INFO:", "score:", self.score])
        except Exception as e:
            print(f"Error: {e}")

    def move(self, head, direction, path):
        path.append(dword[direction])
        self.snake.append(self.grid[head.x+dx[direction]][head.y + dy[direction]])
        self.headV1 = self.snake[-1]
        self.headV2 = self.snake[-2]
        return path

    def moveSnake(self, dir):
        keyboard.press(dir)
        # pyautogui.press(dir)

    def searchApple(self):
        cntApple = 0
        while 1:
            # Sensor con el percibe la posicion de la manzana
            X, Y = self.captureImg.scanRed()
            self.food = self.grid[X-1][Y-1]
            cntApple += 1
            if not (self.food in self.snake):
                break

    def searchHead(self):
        I, J = self.captureImg.scanBlue()
        self.headR1 = self.grid[I-1][J-1]

        # I, J = self.captureImg.scanWhite()
        # self.headR2 = self.grid[I-1][J-1]
    
    def endGame(self):
        return self.captureImg.scanYellow()

### Otra funciones de prueba !!!
    def printBoard(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        x = 1200
        y = 50
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
        width = 408
        height = 360
        wr = width/self.cols
        hr = height/self.rows
        screen = display.set_mode([width, height])
        display.set_caption("snake_self")
        clock = time.Clock()

        # clock.tick(6)
        # Display the grid
        screen.fill(BLACK)
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].show(WHITE, screen, wr, hr)

        # Display the snake
        for node2 in self.snake:
            node2.show(RED, screen, wr, hr)
        self.snake[-1].show(BLUE, screen, wr, hr)

        # Display the food
        self.food.show(GREEN, screen, wr, hr)

        display.flip()
    
    def reset(self):
        # Creacion de la serpiente
        pyautogui.press("enter")
        sleep(0.5)

        # Creacion de la serpiente
        self.lenSanke = 4
        headSnake = self.grid[8][5]
        self.snake = self.createSnake(headSnake.x, headSnake.y, self.lenSanke) # La cabeza es el ultimo elemento
        self.headV1 = self.snake[-1]
        self.headV2 = self.snake[-2]
        self.headR1 = self.snake[-1]
        self.headR2 = self.snake[-2]

        # Posicion inicial de la manzana
        self.food = self.grid[8-1][13-1]
        self.searchApple()

    def times(self, opc, tiempo_inicio, tiempo_limite, name):
        if opc == 0:
            tiempo_inicio = time2.time()
            return tiempo_inicio
        elif opc == 1:
            tiempo_final = time2.time()
            tiempo_ejecucion = tiempo_final - tiempo_inicio
            if tiempo_ejecucion > 0.0:
                print(f"Tiempo de ejecucion {name}: ", tiempo_ejecucion)
            if tiempo_ejecucion >= tiempo_limite:
                print(f"Tiempo de ejecucion excedido {name}")
                sys.exit()
            return int(0)
        
    def playVirtual(self):
        sleep(1)
        clock = time.Clock()
        itr = 0
        try:
            path = []
            direction = 1
            head = self.snake[-1]
            headV = self.snake[-1]

            ## Algoritmos ## Funcion interna de calculo
            dir_array = self.calculate.bfs(self.food, self.snake, self.rows, self.cols)
            
            while 1:
                sleep(0.001)
                clock.tick(6)

                itr += 1
                self.searchHeadVirtual()
                
                print(["INFO:", "score:", self.score, "apple:", self.food.x+1, self.food.y+1, "Itr:", itr])

                if True:                    
                    direction = dir_array.pop(-1)
                    head, headV, path = self.move(head, direction, path)
                    dir = path.pop(0)
                   
                    if head.x == self.food.x and head.y == self.food.y:
                        self.score += 1
                        self.searchAppleVirtual()  ## Sensores

                        ## Algoritmos ## Funcion interna de calculo
                        dir_array = self.calculate.bfs(self.food, self.snake, self.rows, self.cols)

                        # if self.score <= 17:
                        #     dir_array = self.calculate.bfs(self.food, self.snake, self.rows, self.cols)
                        # elif self.score <= 34:
                        #     # dir_array = self.calculate.dfsAll(self.food, self.snake, self.rows, self.cols)
                        #     dir_array = self.calculate.asterisk1(self.food, self.snake, self.grid, self.rows, self.cols)
                        # else:
                        #     if flag == 0:
                        #         dir_array = self.calculate.dfsAll(self.food, self.snake, self.rows, self.cols)
                        #         flag = 1 - flag
                        #     else:
                        #         dir_array = self.calculate.bfs(self.food, self.snake, self.rows, self.cols)
                        #         flag = 1 - flag

                    else:
                        self.snake.pop(0)

                self.printBoard() ## Funcion interna de impresion
                if keyboard.is_pressed("q"):
                    print(["INFO:", "score:", self.score, "apple:", self.food.x+1, self.food.y+1, "Itr:", itr])
                    break
        except Exception as e:
            print(["INFO:", "score:", self.score, "apple:", self.food.x+1, self.food.y+1, "Itr:", itr])
            print(f"Error: {e}")

    def searchAppleVirtual(self):
        import random
        cntApple = 0
        while 1:
            # Sensor con el percibe la posicion de la manzana
            X, Y = random.randint(1, 15), random.randint(1, 17)
            self.food = self.grid[X-1][Y-1]
            cntApple += 1
            if not (self.food in self.snake):
                break
    
    def searchHeadVirtual(self):
        I, J = self.snake[-1].x+1, self.snake[-1].y+1
        self.headR = self.grid[I-1][J-1]
