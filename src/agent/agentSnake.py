from pygame import display, time, init
from time import sleep
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

class IA:
    def __init__(self):
        # Variables de captura de pantalla
        board = monitorObj(left[0], top[0], width[0], height[0])
        self.captureApple = capture(board, wi, hi)
        self.captureHead = capture(board, wi, hi)

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

        # Posicion inicial de la manzana
        self.food = self.grid[8-1][13-1]
        self.searchApple()

        # Instancia del algoritmo
        self.calculate = algorithms()
        
        init()

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
        # clock = time.Clock()
        sleep(1)
        itr = 0
        try:
            path = []
            direction = 1
            head = self.snake[-1]
            headV = self.snake[-1]
            while 1:
                # clock.tick(1)
                itr += 1
                self.searchHead()  ## Sensores

                # Comprobacion de desincronizacion
                if abs(headV.x - self.headR.x) >= lim or abs(headV.y - self.headR.y) >= lim:
                    print(["R:", self.headR.x+1, self.headR.y+1, "v:", headV.x+1, headV.y+1, "Itr:", itr])
                    print(["INFO:", "score:", self.score, "apple:", self.food.x+1, self.food.y+1])
                    print(f"Desincronizacion: i: {abs(headV.x - self.headR.x)} , j: {abs(headV.y - self.headR.y)}")
                    break
                
                # Si la cabeza real y la virtual son iguales se calcula el siguiente movimiento
                if abs(headV.x - self.headR.x) == 0 and abs(headV.y - self.headR.y) == 0:
                    
                    dir_array = self.calculate.bfs(self.food, self.snake, self.grid, self.rows, self.cols)
                    # dir_array = self.calculate.getpath(self.food, self.snake, self.grid, self.rows, self.cols)  ## Funcion interna de calculo
                    direction = dir_array.pop(-1)
                    head, headV, path = self.move(head, direction, path)
                    dir = path.pop(0)
                    
                    self.moveSnake(dir)  ## Actuadores
                    
                    if head.x == self.food.x and head.y == self.food.y:
                        self.score += 1
                        self.searchApple()  ## Sensores
                    else:
                        self.snake.pop(0)

                # self.printBoard() ## Funcion interna de impresion
                if keyboard.is_pressed("q"):
                    break
        except Exception as e:
            print(f"Error: {e}")

    def move(self, head, direction, path):
        path.append(dword[direction])
        self.snake.append(self.grid[head.x+dx[direction]][head.y + dy[direction]])
        return self.snake[-1], self.snake[-1], path

    def moveSnake(self, dir):
        pyautogui.press(dir)

    def searchApple(self):
        cntApple = 0
        while 1:
            # Sensor con el percibe la posicion de la manzana
            X, Y = self.captureApple.scanRed()
            self.food = self.grid[X-1][Y-1]
            cntApple += 1
            if not (self.food in self.snake):
                break

    def searchHead(self):
        I, J = self.captureHead.scanBlue()
        self.headR = self.grid[I-1][J-1]

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

    def hilos(self):
        import threading
        while True:
            # Crear los hilos
            t1 = threading.Thread(target=self.play)
            t2 = threading.Thread(target=self.printBoard)

            # Iniciar los hilos
            t1.start()
            t2.start()

            # Esperar a que terminen los hilos
            t1.join()
            t2.join()
            if keyboard.is_pressed("q"):
                break

    def go(self):
        # opcSensor = 0
        itr = 0
        sleep(2)
        st = 201
        while True:
            itr += 1
            if st == 201:
                self.sensor(0)
            else:
                self.sensor(2)
            dir, st = self.funtion(itr)
            self.actuator(dir, st)
            if keyboard.is_pressed("q") or st == 500:
                break

    def sensor(self, opc):
        if opc == 0:
            self.searchApple()
            self.searchHead()
        elif opc == 1:
            self.searchApple()
        elif opc == 2:
            self.searchHead()

    def funtion(self, cnt):
        try:
            direction = 1
            path = []
            head = self.snake[-1]
            headV = self.snake[-1]
            st = 400
            dir = "0"
            if abs(headV.x - self.headR.x) >= 2 or abs(headV.y - self.headR.y) >= 2:
                print(["v: ", headV.x, headV.y, "R: ", self.headR.x, self.headR.y, cnt, "Score: ", self.score])
                print(f"Desincronizacion: i: {abs(headV.x - self.headR.x)} , j: {abs(headV.y - self.headR.y)}")
                st = 500

            if abs(headV.x - self.headR.x) == 0 and abs(headV.y - self.headR.y) == 0:
                # print(["==","v: ",headV.x, headV.y, "R: ", self.headR.x, self.headR.y, cnt])
                dir_array = self.calculate.getpath(self.food, self.snake, self.grid, self.rows, self.cols)  # Funcion interna de calculo
                direction = dir_array.pop(-1)
                head, headV, path = self.move(head, direction, path)
                dir = path.pop(0)
                st = 200
                if head.x == self.food.x and head.y == self.food.y:
                    self.score += 1
                    st = 201
                else:
                    self.snake.pop(0)
            return dir, st
        except Exception as e:
            print(f"Error: {e}")
            return "0", 500

    def actuator(self, dir, st):
        if st == 200:
            self.moveSnake(dir)  # Actuadores