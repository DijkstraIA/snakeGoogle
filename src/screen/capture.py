import mss
import pyautogui
import cv2
import numpy as np
from time import sleep

sct = mss.mss()

class monitorObj:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class capture:
    def __init__(self, board, wi, hi):

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

    def scanRed(self):
        I = -1
        J = -1
        while True:
            sleep(0.01)
            img =  np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])

            mask = cv2.inRange(hsv, lower_red, upper_red)
            mask = cv2.medianBlur(mask, 5)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
                biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
                M = cv2.moments(biggest_contour)
                if M["m00"] == 0:
                    M["m00"] = 1
                centroid_x = int(M["m10"] / M["m00"])
                centroid_y = int(M["m01"] / M["m00"])

                y = centroid_y
                x = centroid_x
                I = np.floor(y/self.wi) + 1
                J = np.floor(x/self.hi) + 1
                break
        return int(I),int(J)

    def scanWhite(self):
        I = -1
        J = -1
        while True:
            img =  np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_white = np.array([0, 0, 255])
            upper_white = np.array([0, 0, 255])

            mask = cv2.inRange(hsv, lower_white, upper_white)
            mask = cv2.medianBlur(mask, 5)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
                biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
                M = cv2.moments(biggest_contour)
                if M["m00"] == 0:
                    M["m00"] = 1
                centroid_x = int(M["m10"] / M["m00"])
                centroid_y = int(M["m01"] / M["m00"])

                y = centroid_y
                x = centroid_x
                I = np.floor(y/self.wi) + 1
                J = np.floor(x/self.hi) + 1
                # self.printScreen2(img, mask, "White", I, J, x, y)
                return int(I),int(J)

    def scanBlue(self):
        I = -1
        J = -1
        try:
            while True:
                img =  np.array(sct.grab(monitor=self.dim_board))
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_blue = np.array([112, 172, 244])
                upper_blue = np.array([140, 255, 255])

                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                mask = cv2.medianBlur(mask, 5)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
                    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
                    M = cv2.moments(biggest_contour)
                    if M["m00"] == 0:
                        M["m00"] = 1
                    centroid_x = int(M["m10"] / M["m00"])
                    centroid_y = int(M["m01"] / M["m00"])

                    y = centroid_y
                    x = centroid_x
                    I = np.floor(y/self.wi) + 1
                    J = np.floor(x/self.hi) + 1
                    # self.printScreen2(img, mask, "blue", I, J, x, y)
                    return int(I),int(J)
        except:
            print("Error encontrando el azul")
            return -1,-1
        
    def scanBlue2(self):
        I = -1
        J = -1
        try:
            img =  np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Tomo el azul
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
            print("Error encontrando el azul")
            return -1,-1

    def scanYellow(self):
        I = -1
        J = -1
        try:
            if True:
                img =  np.array(sct.grab(monitor=self.dim_board))
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_Yellow = np.array([20, 50, 50])
                upper_Yellow = np.array([30, 255, 255])

                mask = cv2.inRange(hsv, lower_Yellow, upper_Yellow)
                mask = cv2.medianBlur(mask, 5)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    return True
                    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
                    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
                    M = cv2.moments(biggest_contour)
                    if M["m00"] == 0:
                        M["m00"] = 1
                    centroid_x = int(M["m10"] / M["m00"])
                    centroid_y = int(M["m01"] / M["m00"])

                    y = centroid_y
                    x = centroid_x
                    I = np.floor(y/self.wi) + 1
                    J = np.floor(x/self.hi) + 1
                    # self.printScreen2(img, mask, "yelow", I, J, x, y)
                    return int(I),int(J)
            return False
        except:
            print("Error encontrando el azul")
            return -1,-1

    def mousePosition(self):
        cnt = 0
        while cnt < 100:
            print(pyautogui.position())
            cnt += 1

    def printScreen2(self, img, mask, color, I, J, x, y):
        cv2.circle(img, (x,y), 3, (255,0,255),-1)
        cv2.putText(img, f"({I}, {J})", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow(f"Imagen con color {color}", img)
        # cv2.imshow(f"mask {color}", mask)
        cv2.waitKey(1)

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
        

