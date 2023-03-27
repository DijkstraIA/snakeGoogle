import mss
import pyautogui
import cv2
import numpy as np

sct = mss.mss()

class capture:
    def __init__(self):
        # self.board
        # self.result

        #Dimensiones del tablero
        self.dim_board = {
                'left': 35,
                'top': 212,
                'width': 680,
                'height': 610
        }

        #Dimensiones de la manzana
        self.wapple = 20
        self.happle = 20 
        self.dim_apple = {
                'left': 527, #515,
                'top': 505, #483,
                'width': self.wapple,
                'height': self.happle
        }

        #Captura de la manzana
        self.apple =  np.array(sct.grab(monitor=self.dim_apple))
        self.per  = .75
    
        #Variables para Calculo de casilla
        self.w, self.h = pyautogui.size()
        self.eps = 3
        self.disSquard = 40
        self.iniX = 12
        self.iniY = 10

    def scan(self, i,j):
        X = i
        Y = j
        board =  sct.grab(monitor=self.dim_board)
        self.board = np.array(board)        
        
        #Procesar imagen buscando apple
        self.result = cv2.matchTemplate(board, self.apple, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(self.result)

        if max_val > self.per:
            #Calculo de la casilla
            Y = np.round(((max_loc[0])-self.iniX)/self.disSquard + 1)
            X = np.round(((max_loc[1])-self.iniY)/self.disSquard + 1)
        return int(X),int(Y)
    
    def printScreen(self):
        cv2.imshow("Computer object", self.apple)
        cv2.imshow("Computer result", self.result)

        yloc, xloc = np.where(self.result >= self.per)
        print(len(xloc))
        for(x,y) in zip(xloc, yloc):
            cv2.rectangle(self.board, (x,y), (x + self.wapple, y + self.happle), (0,255,255), 2)
                        
        small = cv2.resize(self.board, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("Computer Vision", small)
        

