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
top = [212,505]
width = [680,20]
height = [610,20]

class IA:
    def __init__(self):
        board = monitorObj(left[0], top[0], width[0], height[0])
        apple = monitorObj(left[1], top[1], width[1], height[1])
        self.captureApple = capture(board,apple)
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

    def play(self):
        cnt = 0
        # clock = time.Clock()
        print([self.score, cnt])
        try:
            direction = 1
            self.searchApple() ##Sensores
            head = self.snake[-1]
            path = []
            while 1:
                cnt+=1
                if head.x == head.x and head.y == head.y and self.score <= 10:
                    # print([cnt, self.score, direction, head.x, head.y, self.food.x, self.food.y ])
                    dir_array = self.asterisk.getpath(self.food, self.snake, self.grid, self.rows, self.cols) ##Funcion interna de calculo
                    direction = dir_array.pop(-1)
                    head, path = self.move(head, direction, path)
                    if head.x == self.food.x and head.y == self.food.y:
                        print(path)
                        for dir in path:
                            # clock.tick(11)
                            self.moveSnake(dir) ##Actuadores que generan acciones
                            # sleep(.04)
                        path = []
                        self.score += 1
                        self.searchApple()
                    else:
                        self.snake.pop(0)
                else:
                    #TODO: Capture head snake
                    print("Game Over")
                    break
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
        return self.snake[-1], path
    
    def moveSnake(self, dir):
        pyautogui.press(dir)

    def searchApple(self):
        while 1:
            X,Y = self.captureApple.scan(self.food.x,self.food.y) #Sensor con el percibe la posicion de la manzana
            self.food = self.grid[X-1][Y-1]
            if not (self.food in self.snake):
                break
    
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
        
        clock.tick(6)
        # Display the grid
        screen.fill(BLACK)
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].show(WHITE)

        # Display the snake
        for point in self.snake:
            point.show(RED)
        self.snake[-1].show(BLUE)

        # Display the food
        self.food.show(GREEN)

        display.flip()

    
    
