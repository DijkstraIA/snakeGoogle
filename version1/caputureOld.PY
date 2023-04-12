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
    def __init__(self, board, objectSearch, wi, hi, per=.75):

        #Dimensiones del tablero
        self.dim_board = {
                'left': board.left,
                'top': board.top, 
                'width': board.width,
                'height': board.height
        }
        #Dimensiones de una casilla
        self.wi = wi
        self.hi = hi

        #Dimensiones de la manzana
        self.wobject = objectSearch.width 
        self.hobject = objectSearch.height  
        self.dim_object = {
                'left': objectSearch.left,
                'top': objectSearch.top, 
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
    
    def scanRed(self):
        I = -1
        J = -1
        while True:
            img =  np.array(sct.grab(monitor=self.dim_board))
            #Toma el rojo
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            whilte_point = cv2.findNonZero(mask)

            if whilte_point is not None and whilte_point[0] is not None and whilte_point[0][0] is not None:
                ind = int(len(whilte_point)//3)
                x = whilte_point[ind][0][0]
                y = whilte_point[ind][0][1]
                I = np.floor(y/self.wi) + 1
                J = np.floor(x/self.hi) + 1              
                break
        return int(I),int(J)

    
    def scanWhite(self):
        I = -1
        J = -1
        while True:
            img =  np.array(sct.grab(monitor=self.dim_board))
            
            # Convierte la imagen a escala de grises
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Aplica una umbralización para detectar los píxeles blancos
            _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
            
            whilte_point = cv2.findNonZero(thresh)

            if whilte_point is not None and whilte_point[0] is not None and whilte_point[0][0] is not None:
                ind = int(len(whilte_point)//2)

                x = whilte_point[ind][0][0]
                y = whilte_point[ind][0][1]
                
                I = np.floor(y/self.wi) + 1
                J = np.floor(x/self.hi) + 1
                # print([x,y])
                # print(["CON: ",I,J])s
                # cv2.circle(img, (x,y), 2, (255,0,255),-1)
                # # Muestra la imagen resultante
                # cv2.imshow("Imagen con contornos", img)
                # cv2.waitKey(1)
            if I != -1 and J != -1:
                break
        return int(I),int(J)

    def scanBlue(self):
        I = -1
        J = -1
        try:
            img =  np.array(sct.grab(monitor=self.dim_board))
            # Tomo el azul
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_red = np.array([112, 172, 244])
            upper_red = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            whilte_point = cv2.findNonZero(mask)
            ind = int(len(whilte_point)//3)
            x = whilte_point[ind][0][0]
            y = whilte_point[ind][0][1]
            I = np.floor(y/self.wi) + 1
            J = np.floor(x/self.hi) + 1
            return int(I),int(J)
        except:
            print("Error sacando el azul")
            return -1,-1

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
        

