from time import sleep
import numpy as np
import pyautogui
import mss
import cv2

sct = mss.mss()

class monitorObj:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class capture:
    def __init__(self, board, wi, hi):

        # Dimensiones del tablero
        self.dim_board = {
            'left': board.left,
            'top': board.top,
            'width': board.width,
            'height': board.height
        }
        # Dimensiones de una casilla
        self.wi = wi
        self.hi = hi

    def scanRed(self):
        I = -1
        J = -1
        itr = 0
        while itr < 100:
            itr = itr + 1
            img = np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Toma el rojo
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
        return int(I), int(J)

    def scanRedV2(self):
        I = -1
        J = -1
        itr = 0
        while itr < 100:
            itr = itr + 1
            sleep(0.01)
            img = np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])

            mask = cv2.inRange(hsv, lower_red, upper_red)
            mask = cv2.medianBlur(mask, 5)
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                contour_sizes = [(cv2.contourArea(contour), contour)
                                 for contour in contours]
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
        return int(I), int(J)

    def scanBlue(self):
        I = -1
        J = -1
        itr = 0
        color_objetivo = (78, 124, 246)
        try:
            while itr < 100:
                itr+=1
                img = np.array(sct.grab(monitor=self.dim_board))

                # Convertir la imagen a espacio de color RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # Encontrar los puntos donde existe el color objetivo
                puntos = np.where(np.all(img_rgb == color_objetivo, axis=-1))

                # Seleccionar el punto más centrado del área conformada por los puntos
                if puntos is not None and len(puntos[0]) > 0:
                    # Obtener las coordenadas de los puntos encontrados
                    coords = list(zip(puntos[1], puntos[0]))

                    # Calcular el punto más centrado del área conformada por los puntos
                    centro_x = np.mean([p[0] for p in coords])
                    centro_y = np.mean([p[1] for p in coords])
                    punto_central = (int(centro_x), int(centro_y))

                    x, y = punto_central

                    I = np.floor(y/self.wi) + 1
                    J = np.floor(x/self.hi) + 1

                    return int(I), int(J)
            return -1, -1
        except:
            # print("Error encontrando el azul")
            return -1, -1

    def printScreen(self):
        w, h = pyautogui.size()
        print("Screen Resolution: " + str(w) + 'x' + str(h))
        cv2.imshow("Computer object", self.object)
        cv2.imshow("Computer result", self.result)

        yloc, xloc = np.where(self.result >= self.per)
        print(len(xloc))
        for (x, y) in zip(xloc, yloc):
            cv2.rectangle(self.board, (x, y), (x + self.wobject,
                          y + self.hobject), (0, 255, 255), 2)

        small = cv2.resize(self.board, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("Computer Vision", small)

    
    def printScreen2(self, img, mask, color, I, J, x, y):
        cv2.circle(img, (x, y), 3, (255, 0, 255), -1)
        cv2.putText(img, f"({I}, {J})", (int(x), int(
            y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow(f"Imagen con color {color}", img)
        cv2.imshow(f"mask {color}", mask)
        cv2.waitKey(1)