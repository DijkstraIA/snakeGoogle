from pygame import display, time, init
from time import sleep
import pyautogui
import keyboard
import os

from agent.algorithm import asterisk
from model.piece import Point
from screen.capture import capture, monitorObj

# [board, apple]
left = [35,527]
top = [217,505]
width = [680,20]
height = [600,20]

# Tamaño de la casilla en pixeles
wi = 40
hi = 40

class IA:
    def __init__(self):
        board = monitorObj(left[0], top[0], width[0], height[0])
        apple = monitorObj(left[1], top[1], width[1], height[1])
        self.captureApple = capture(board, apple, wi, hi)
        self.captureHead = capture(board, apple, wi, hi)
        self.asterisk = asterisk()
        self.lenSanke = 4
        self.score = 0
        self.rows = 15
        self.cols = 17
        self.grid = [[Point(i, j) for j in range(self.cols)] for i in range(self.rows )]
        self.createGraph()
        self.food = self.grid[8-1][13-1]
        headSnake = self.grid[8][5]
        # headSnake = self.searchHead()
        self.snake = self.createSnake(headSnake.x, headSnake.y, self.lenSanke) #TODO Capture head snake
        self.searchApple()
        self.headR = self.searchHead() 
        init()

    def createSnake(self, iniI, iniJ, lenSanke):
        snake = []
        for k in reversed(range(lenSanke)):
            snake.append(self.grid[iniI-1][iniJ-1-k])
        return snake

    def createGraph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].add_neighbors(self.grid, self.rows, self.cols)

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
        opcSensor = 0
        opcFunction = 0
        opcActuator = 0
        while True:
            self.sensor(0)
            self.funtion(0)
            self.actuator(0)
            if keyboard.is_pressed("q"):
                break
    
    def sensor(self, opc = 0):
        if opc == 0:
            self.searchHead()
            self.searchApple()
        elif opc == 1:
            self.searchApple()
        elif opc == 2:
            self.searchHead()

    def play(self):
        cnt = 0
        # clock = time.Clock()
        try:
            direction = 1
            path = []
            self.searchApple() ##Sensores
            head = self.snake[-1]
            headV = self.snake[-1]
            headR = self.searchHead() ##Sensores
            while 1:
                cnt+=1
                # clock.tick(1)
                headR = self.searchHead() ##Sensores
                if abs(headV.x - headR.x) >= 2 or abs(headV.y - headR.y) >= 2:
                    print(["v: ",headV.x, headV.y, "R: ", headR.x, headR.y, cnt, "Score: ", self.score])
                    print(f"Desincronizacion: i: {abs(headV.x - headR.x)} , j: {abs(headV.y - headR.y)}")
                    break

                if abs(headV.x - headR.x) == 0 and abs(headV.y - headR.y) == 0:
                    # print(["==","v: ",headV.x, headV.y, "R: ", headR.x, headR.y, cnt])
                    dir_array = self.asterisk.getpath(self.food, self.snake, self.grid, self.rows, self.cols) ##Funcion interna de calculo
                    direction = dir_array.pop(-1)
                    head, headV, path = self.move(head, direction, path)
                    dir = path.pop(0)
                    self.moveSnake(dir) ## Actuadores
                    if head.x == self.food.x and head.y == self.food.y:
                        self.score += 1
                        self.searchApple() ##Sensores
                    else:
                        self.snake.pop(0)
                if keyboard.is_pressed("q"):
                    break
        except Exception as e:
            print(f"Error: {e}")

    def move(self, head, direction, path):
        if direction == 0:    # down
            path.append("right")
            self.snake.append(self.grid[head.x][head.y + 1])
        elif direction == 1:  # right
            path.append("down")
            self.snake.append(self.grid[head.x + 1][head.y])
        elif direction == 2:  # up
            path.append("left")
            self.snake.append(self.grid[head.x][head.y - 1])
        elif direction == 3:  # left
            path.append("up")
            self.snake.append(self.grid[head.x - 1][head.y])
        return self.snake[-1],self.snake[-1], path
    
    def moveSnake(self, dir):
        pyautogui.press(dir)

    def searchApple(self):
        cntApple = 0
        while 1:
            X,Y = self.captureApple.scanRed() #Sensor con el percibe la posicion de la manzana
            self.food = self.grid[X-1][Y-1]
            cntApple += 1
            if not (self.food in self.snake):
                # print(f"Apple: {cntApple}")
                break
    
    def searchHead(self):
        I, J = self.captureHead.scanBlue()
        return self.grid[I-1][J-1]
    
    def printBoard(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        x = 1200
        y = 50
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
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
        for point in self.snake:
            point.show(RED, screen, wr, hr)
        self.snake[-1].show(BLUE, screen, wr, hr)

        # Display the food
        self.food.show(GREEN, screen, wr, hr)

        display.flip()

    
    
