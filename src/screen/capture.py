import mss
import pyautogui
import cv2
import numpy as np

sct = mss.mss()

class monitorObj:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class capture:
    def __init__(self, board, objectSearch, per=.75):

        #Dimensiones del tablero
        self.dim_board = {
                'left': board.left, #35
                'top': board.top, #212	
                'width': board.width, #680
                'height': board.height #610
        }

        #Dimensiones de la manzana
        self.wobject = objectSearch.width #20
        self.hobject = objectSearch.height #20 
        self.dim_object = {
                'left': objectSearch.left, #527
                'top': objectSearch.top ,#505
                'width': self.wobject,
                'height': self.hobject
        }

        #Captura de la manzana
        self.object =  np.array(sct.grab(monitor=self.dim_object))
        self.per  = per
    
        #Variables para Calculo de casilla
        #self.w, self.h = pyautogui.size()
        self.eps = 3
        self.disSquard = 40
        self.iniX = 12
        self.iniY = 10

    def scan(self, i,j):
        X = i
        Y = j
        board =  sct.grab(monitor=self.dim_board)
        self.board = np.array(board)        
        
        #Procesar imagen buscando object
        self.result = cv2.matchTemplate(self.board, self.object, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(self.result)

        if max_val > self.per:
            #Calculo de la casilla
            Y = np.round(((max_loc[0])-self.iniX)/self.disSquard + 1)
            X = np.round(((max_loc[1])-self.iniY)/self.disSquard + 1)
        return int(X),int(Y)
    
    def mousePosition(self):
        cnt = 0
        while cnt < 100:
            print(pyautogui.position())
            cnt += 1

    def printScreen(self):
        w, h = pyautogui.size()
        print("Screen Resolution: " + str(w) + 'x' + str(h))
        cv2.imshow("Computer object", self.object)
        cv2.imshow("Computer result", self.result)

        yloc, xloc = np.where(self.result >= self.per)
        print(len(xloc))
        for(x,y) in zip(xloc, yloc):
            cv2.rectangle(self.board, (x,y), (x + self.wobject, y + self.hobject), (0,255,255), 2)
                        
        small = cv2.resize(self.board, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("Computer Vision", small)
        
