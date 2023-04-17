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

    def scanRedV2(self):
        I = -1
        J = -1
        while True:
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

    def scanRedV3(self):
        I = -1
        J = -1
        path = "C:/Users/lfmen/OneDrive/Documentos/Universidad/SistemasInteligentes/snakeGoogleV3SIFT/version1"
        dir = f"{path}/nose.png"

        # Cargar la imagen de referencia
        template = cv2.imread(dir, 0)
        h, w = template.shape

        while True:
            img = np.array(sct.grab(monitor=self.dim_board))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Realizar template matching
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(res >= threshold)

            # Obtener el primer punto encontrado y dibujar el rectángulo
            if loc[0].size > 0 and loc[1].size > 0:
                pt = (loc[1][0], loc[0][0])
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

                x = pt[0]
                y = pt[1]
                # Dibujar el punto clave
                I = np.floor(y/self.wi) + 1
                J = np.floor(x/self.hi) + 1

            print(I, J)
            return int(I), int(J)

    def scanRed(self):
        I = -1
        J = -1
        while True:
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

    def scanWhite(self):
        I = -1
        J = -1
        while True:
            img = np.array(sct.grab(monitor=self.dim_board))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_white = np.array([0, 0, 255])
            upper_white = np.array([0, 0, 255])

            mask = cv2.inRange(hsv, lower_white, upper_white)
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
                # self.printScreen2(img, mask, "White", I, J, x, y)
                return int(I), int(J)

    def scanBlueV2(self):
        I = -1
        J = -1
        try:
            while True:
                img = np.array(sct.grab(monitor=self.dim_board))
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_blue = np.array([112, 172, 244])
                upper_blue = np.array([140, 255, 255])

                mask = cv2.inRange(hsv, lower_blue, upper_blue)
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
                    # self.printScreen2(img, mask, "blue", I, J, x, y)
                    return int(I), int(J)
        except:
            print("Error encontrando el azul")
            return -1, -1

    def scanBlueV3(self):
        I = -1
        J = -1

        # Especifica los límites inferior y superior del rango de colores rojos en formato HSV
        rojo_bajo = np.array([0, 70, 50])
        rojo_alto = np.array([10, 255, 255])

        # Cargar la imagen de referencia en escala de grises
        path = "C:/Users/lfmen/OneDrive/Documentos/Universidad/SistemasInteligentes/snakeGoogleV3/version1"
        dir = f"{path}/nariz.png"
        head_ref = cv2.imread(dir, cv2.IMREAD_GRAYSCALE)

        # Crear un objeto SIFT
        sift = cv2.xfeatures2d.SIFT_create()

        try:
            while True:
                img = np.array(sct.grab(monitor=self.dim_board))

                # Convertir la imagen capturada a escala de grises
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Detectar keypoints y descriptores en la imagen capturada
                kp1, des1 = sift.detectAndCompute(gray, None)

                # Detectar keypoints y descriptores en la imagen de referencia
                kp2, des2 = sift.detectAndCompute(head_ref, None)

                # Realizar la coincidencia de puntos usando fuerza bruta
                bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
                matches = bf.match(des1, des2)
                matches = sorted(matches, key=lambda x: x.distance)

                # Obtener el punto de coincidencia más grande
                if len(matches) > 0:
                    match = matches[0]
                    x, y = kp1[match.queryIdx].pt
                    x, y = int(x), int(y)

                    # Aplicar la máscara de rango de colores rojos
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, rojo_bajo, rojo_alto)
                    if mask[y, x] == 0:  # Si el punto no está en el rango de rojos
                        # Dibujar un rectángulo alrededor del punto de coincidencia más grande
                        I = np.floor(y/self.wi) + 1
                        J = np.floor(x/self.hi) + 1
                        # cv2.rectangle(img, (x-10, y-10), (x+10, y+10), (0, 255, 0), 2)
                        cv2.putText(img, f"({I} , {J})", (x+20, y-20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        print(f"{I , J}]")
                        return int(I), int(J)
        except:
            print("Error encontrando el azul")
            return -1, -1

    def scanBlueV4(self):
        I = -1
        J = -1
        color_objetivo = (78, 124, 246)
        try:
            while True:
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

                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        except:
            print("Error encontrando el azul")
            return -1, -1

    def scanBlue(self):
        I = -1
        J = -1
        try:
            img = np.array(sct.grab(monitor=self.dim_board))
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
            return int(I), int(J)
        except:
            # print("Error encontrando el azul")
            return -1, -1

    def scanYellow(self):
        I = -1
        J = -1
        try:
            if True:
                img = np.array(sct.grab(monitor=self.dim_board))
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_Yellow = np.array([20, 50, 50])
                upper_Yellow = np.array([30, 255, 255])

                mask = cv2.inRange(hsv, lower_Yellow, upper_Yellow)
                mask = cv2.medianBlur(mask, 5)
                contours, _ = cv2.findContours(
                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    return True
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
                    # self.printScreen2(img, mask, "yelow", I, J, x, y)
                    return int(I), int(J)
            return False
        except:
            print("Error encontrando el azul")
            return -1, -1

    def mousePosition(self):
        cnt = 0
        while cnt < 100:
            print(pyautogui.position())
            cnt += 1

    def printScreen2(self, img, mask, color, I, J, x, y):
        cv2.circle(img, (x, y), 3, (255, 0, 255), -1)
        cv2.putText(img, f"({I}, {J})", (int(x), int(
            y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
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
        for (x, y) in zip(xloc, yloc):
            cv2.rectangle(self.board, (x, y), (x + self.wobject,
                          y + self.hobject), (0, 255, 255), 2)

        small = cv2.resize(self.board, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("Computer Vision", small)
