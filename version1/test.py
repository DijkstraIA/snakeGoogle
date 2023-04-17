import cv2
import mss
import numpy as np
import pyautogui
import keyboard
from pygame import time

# dim_board = {
#         'left': 35,
#         'top': 217,
#         'width': 680,
#         'height': 600
#     }
dim_board = {
    'left': 35,
    'top': 257,  # Aqui modifique de 217 (sebastian) a 257 (luis)
    'width': 680,
    'height': 600
}

# Carga una imagen de muestra del juego Snake Arcade
# board =  sct.grab(monitor=dim_board)
# board = np.array(board)
# path = "C:/Users/sebas/OneDrive/Escritorio/Inteligentes/snakeGoogle/version1"
# dir = f"{path}/apple.png"
# pyautogui.PAUSE = 0

ini = "s"
end = "q"
print("Press " + ini + " to start playing.")
print("Once started press " + end + " to quit.")
keyboard.wait(ini)

eps = 3
disSquard = 40
iniX = 12
iniY = 10
wi = 40
hi = 40

# # Especifica los límites inferior y superior del rango de colores rojos en formato HSV
# rojo_bajo = np.array([0, 70, 50])
# rojo_alto = np.array([10, 255, 255])

# # Cargar la imagen de referencia en escala de grises
# path = "C:/Users/lfmen/OneDrive/Documentos/Universidad/SistemasInteligentes/snakeGoogleV3/version1"
# dir = f"{path}/nariz.png"
# head_ref = cv2.imread(dir, cv2.IMREAD_GRAYSCALE)

# # Crear un objeto SIFT
# sift = cv2.xfeatures2d.SIFT_create()

# # Detectar puntos clave y calcular descriptores en la imagen de referencia
# keypoints_ref, descriptores_ref = sift.detectAndCompute(head_ref, None)

# umbral_distancia = 0.7  # Ajusta este valor según sea necesario

# path = "C:/Users/lfmen/OneDrive/Documentos/Universidad/SistemasInteligentes/snakeGoogleV3SIFT/version1"
# dir = f"{path}/nose.png"

# # Cargar la imagen de referencia
# template = cv2.imread(dir, 0)
# h, w = template.shape

clock = time.Clock()

color_objetivo = (78, 124, 246)

while True:

    sct = mss.mss()
    img = np.array(sct.grab(monitor=dim_board))

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convertir# Encontrar los puntos donde existe el color objetivo
    puntos = np.where(np.all(img_rgb == color_objetivo, axis=-1))

    # Seleccionar el punto más centrado del área conformada por los puntos
    if puntos[0].size > 0:
        # Obtener las coordenadas de los puntos encontrados
        coords = list(zip(puntos[1], puntos[0]))

        # Calcular el punto más centrado del área conformada por los puntos
        centro_x = np.mean([p[0] for p in coords])
        centro_y = np.mean([p[1] for p in coords])
        punto_central = (int(centro_x), int(centro_y))

        x, y = punto_central

        # Dibujar un círculo en el punto céntrico de color rojo (BGR)
        img = cv2.circle(img, punto_central, 5, (0, 0, 255), -1)

        I = np.floor(y/wi) + 1
        J = np.floor(x/hi) + 1

    cv2.imshow('Imagen', img)
    cv2.waitKey(1)
    if keyboard.is_pressed(end):
        cv2.destroyAllWindows

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Realizar template matching
    # res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.9
    # loc = np.where(res >= threshold)

    # # Obtener el primer punto encontrado y dibujar el rectángulo
    # if loc[0].size > 0 and loc[1].size > 0:
    #     pt = (loc[1][0], loc[0][0])
    #     cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    #     x = pt[0]
    #     y = pt[1]
    #     # Dibujar el punto clave
    #     I = np.floor(y/wi) + 1
    #     J = np.floor(x/hi) + 1

    #     cv2.putText(img, f"[{I} , {J}]", (pt[0], pt[1] - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # cv2.imshow("Template Matching", img)

    # # Convertir la imagen capturada a escala de grises
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Detectar keypoints y descriptores en la imagen capturada
    # kp1, des1 = sift.detectAndCompute(gray, None)

    # # Detectar keypoints y descriptores en la imagen de referencia
    # kp2, des2 = sift.detectAndCompute(head_ref, None)

    # # Realizar la coincidencia de puntos usando fuerza bruta
    # bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    # matches = bf.match(des1, des2)
    # matches = sorted(matches, key=lambda x: x.distance)

    # # Obtener el punto de coincidencia más grande
    # if len(matches) > 0:
    #     match = matches[0]
    #     x, y = kp1[match.queryIdx].pt
    #     x, y = int(x), int(y)

    #     # Aplicar la máscara de rango de colores rojos
    #     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(hsv, rojo_bajo, rojo_alto)
    #     if mask[y, x] == 0:  # Si el punto no está en el rango de rojos
    #         # Dibujar un rectángulo alrededor del punto de coincidencia más grande
    #         centro_x = x
    #         centro_y = y
    #         I = np.floor(centro_y/wi) + 1
    #         J = np.floor(centro_x/hi) + 1
    #         # cv2.rectangle(img, (x-10, y-10), (x+10, y+10), (0, 255, 0), 2)
    #         cv2.putText(img, f"({I} , {J})", (x+20, y-20),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # # Mostrar la imagen resultante
    # cv2.imshow("Imagen con contorno", img)

    # img = cv2.imread(dir)

    # Convierte la imagen a escala de grises
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Tomo el blanco
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower_red = np.array([0, 0, 200])
    # upper_red = np.array([180, 30, 255])
    # mask = cv2.inRange(hsv, lower_red, upper_red)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('frame', img)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    # cv2.waitKey(1)
    # # cv2.destroyAllWindows()
    # if keyboard.is_pressed(end):
    #     break

    # # Tomo el azul
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # lower_red = np.array([100, 100, 100])
    # # upper_red = np.array([140, 255, 255])
    # lower_blue = np.array([112, 172, 244])
    # upper_blue = np.array([140, 255, 255])
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(1)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('frame', img)
    # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # mx = [0,0,0]
    # mn = [255,255,255]
    # for i in range(0, len(hsv)):
    #     for j in range(0, len(hsv[0])):
    #         if hsv[i][j][0] > mx[0] and hsv[i][j][1] > mx[1] and hsv[i][j][2] > mx[2]:
    #             mx = hsv[i][j]
    #         if hsv[i][j][0] <= mn[0] and hsv[i][j][1] <= mn[1] and hsv[i][j][2] <= mn[2]:
    #             mn = hsv[i][j]
    # print(mn)
    # print(mx)
    # break
    # cv2.imshow('res', res)
    # cv2.destroyAllWindows()
    # if keyboard.is_pressed(end):
    #     break

    # Tomo el azul v2
    # Cargar la imagen desde un archivo PNG.
    # img = cv2.imread("ruta/a/la/imagen.png")

    # # Convertir la imagen de formato BGR a formato HSV.
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # Definir el rango de color azul.
    # # lower_blue = np.array([112, 172, 244])
    # lower_blue = np.array([0, 0, 255])
    # upper_blue = np.array([0, 0, 255])
    # mx = [0,0,0]
    # mn = [255,255,255]
    # # for i in range(0, len(hsv)):
    # #     for j in range(0, len(hsv[0])):
    # #         if hsv[i][j][0] > mx[0] and hsv[i][j][1] > mx[1] and hsv[i][j][2] > mx[2]:
    # #             mx = hsv[i][j]
    # #         if hsv[i][j][0] <= mn[0] and hsv[i][j][1] <= mn[1] and hsv[i][j][2] <= mn[2]:
    # #             mn = hsv[i][j]
    # # print("min: ", mn)
    # # print("max", mx)

    # # Crear un filtro de color para extraer solo los píxeles azules dentro del rango de color especificado.
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('mask', mask)
    # # cv2.waitKey(1)
    # # Encontrar el punto más azul dentro de la imagen filtrada.
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # if len(contours) > 0:
    #     cnt = max(contours, key=cv2.contourArea)
    #     (x, y), _ = cv2.minEnclosingCircle(cnt)

    #     # Convertir las coordenadas de píxeles a coordenadas en la retícula.
    #     rows = 15
    #     cols = 17
    #     x_grid = int(x / (img.shape[1] / cols)) + 1
    #     y_grid = int(y / (img.shape[0] / rows)) + 1

    #     # Mostrar el punto más azul y su coordenada en la retícula en la imagen original.
    #     cv2.circle(img, (int(x), int(y)), 1, (255, 0, 0), -1)
    #     cv2.putText(img, f"({x_grid}, {y_grid})", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    #     # cv2.imshow("Imagen", img)
    #     # cv2.waitKey(1)

    # Tomo punto fijo en el azul
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower_blue = np.array([112, 172, 244])
    # upper_blue = np.array([140, 255, 255])
    # # lower_blue = np.array([0, 0, 255])
    # # upper_blue = np.array([0, 0, 255])

    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # # Aplicar un filtro de mediana para reducir el ruido en la imagen filtrada.
    # mask = cv2.medianBlur(mask, 5)
    # cv2.imshow('mask', mask)
    # contours, _ = cv2.findContours(
    #     mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # if len(contours) > 0:
    #     contour_sizes = [(cv2.contourArea(contour), contour)
    #                      for contour in contours]
    #     biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    #     # print("True")
    #     M = cv2.moments(biggest_contour)
    #     if M["m00"] == 0:
    #         M["m00"] = 1
    #     centroid_x = int(M["m10"] / M["m00"])
    #     centroid_y = int(M["m01"] / M["m00"])
    #     cv2.circle(img, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
    #     y = centroid_y
    #     x = centroid_x
    #     I = np.floor(y/wi) + 1
    #     J = np.floor(x/hi) + 1
    #     cv2.putText(img, f"({I}, {J})", (int(x), int(
    #         y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # else:
    #     print("No se ha encontrado ningún contorno en la imagen")

    # print(["CON: ",I,J])

    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    # #Toma el rojo
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower_red = np.array([0, 100, 100])
    # upper_red = np.array([10, 255, 255])
    # # lower_red = np.array([40, 166, 209])
    # # upper_red = np.array([10, 255, 255])
    # mask = cv2.inRange(hsv, lower_red, upper_red)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('frame', img)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()
    # mx = [0,0,0]
    # mn = [255,255,255]
    # for i in range(0, len(hsv)):
    #     for j in range(0, len(hsv[0])):
    #         if hsv[i][j][0] > mx[0] and hsv[i][j][1] > mx[1] and hsv[i][j][2] > mx[2]:
    #             mx = hsv[i][j]
    #         if hsv[i][j][0] <= mn[0] and hsv[i][j][1] <= mn[1] and hsv[i][j][2] <= mn[2]:
    #             mn = hsv[i][j]
    # print(mn)
    # print(mx)
    # break
    # if keyboard.is_pressed(end):
    #     break

    # # blanco 2
    # img =  np.array(sct.grab(monitor=dim_board))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # Obtener el valor máximo de intensidad de píxeles en la imagen
    # max_val = np.max(img)

    # # Crear una imagen binaria que contenga solo los píxeles que tienen el valor máximo de intensidad
    # binary_img = np.zeros_like(img)
    # binary_img[img == max_val] = 255

    # # Aplicar erosión y dilatación para eliminar el ruido
    # kernel = np.ones((5, 5), np.uint8)
    # binary_img = cv2.erode(binary_img, kernel, iterations=1)
    # binary_img = cv2.dilate(binary_img, kernel, iterations=1)

    # # Encontrar los contornos de los objetos en la imagen binaria
    # contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Dibujar los contornos encontrados en la imagen original
    # img_contours = cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    # # Mostrar la imagen
    # cv2.imshow('Imagen con el blanco más claro resaltado', img_contours)
    # cv2.waitKey(1)

    # # Aplica una umbralización para detectar los píxeles blancos
    # ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)

    # # Encuentra los contornos de los objetos en la imagen
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # whilte_point = cv2.findNonZero(mask)
    # if whilte_point is not None and whilte_point[0] is not None and whilte_point[0][0] is not None:
    # # if True:
    #     # print(whilte_point[0])
    #     # print(type(whilte_point[0]))
    #     # clock.tick(6)
    #     print(len(whilte_point))
    #     ind = int(len(whilte_point)-1)
    #     x = whilte_point[ind][0][0]
    #     y = whilte_point[ind][0][1]
    #     # print([x,y])

    #     # Y = np.round(((x)-iniX)/disSquard + 1)
    #     # X = np.round(((y)-iniY)/disSquard + 1)
    #     # I = np.round(y/wi) + 1
    #     # J = np.sround(x/hi) + 1
    #     I = np.floor(y/wi) + 1
    #     J = np.floor(x/hi) + 1
    #     print(["CON: ",I,J])
    #     cv2.circle(img, (x,y), 2, (255,0,255),-1)

    # # Dibuja los contornos detectados en la imagen original
    # # cv2.drawContours(img, whilte_point, -1, (0, 0, 255), 2)

    # # ## Codigo para capturar los pixeles blancos
    # # # Crear una máscara que contenga solo los píxeles blancos
    # # lower_white = np.array([200, 200, 200])
    # # upper_white = np.array([255, 255, 255])
    # # print(len(lower_white))
    # # print(len(upper_white))
    # # mask = cv2.inRange(img, lower_white, upper_white)

    # # # Encontrar las coordenadas de los píxeles no cero en la máscara
    # # white_pixels = cv2.findNonZero(mask)

    # # # Mostrar las coordenadas de los píxeles blancos en la imagen
    # # print(white_pixels)
    # # ## ------------------------------


# # Crea un objeto ORB
# orb = cv2.ORB_create()

# dir2 = f"{path}/head.png"
# # Carga la imagen del elemento que deseas detectar
# elemento = cv2.imread(dir2)

# # Detecta las características ORB de la imagen completa
# kp2, des2 = orb.detectAndCompute(img, None)

# # Detecta las características ORB del elemento
# kp1, des1 = orb.detectAndCompute(elemento, None)

# # Empareja las características ORB del elemento con las características ORB de la imagen completa
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# matches = bf.match(des1, des2)

# # # Dibuja los puntos clave ORB en la imagen
# img_kp = cv2.drawKeypoints(img, kp2, None, color=(0,255,0), flags=0)

# # Ordena los puntos clave ORB emparejados en función de su distancia
# matches = sorted(matches, key=lambda x:x.distance)

# # Dibuja los puntos clave ORB del elemento en la imagen completa
# img_matches = cv2.drawMatches(elemento, kp1, img, kp2, matches[:10], None, flags=2)

# # Muestra la imagen con los puntos clave ORB dibujados
# cv2.imshow("Snake Arcade", img_matches)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# Problema:
#     Desincronizacion entre el ambiente y la memoria interna (reticula)

# Lluvia de ideas
#     Cancelar la asignatura
#     WebScraping con selenium
#     Algortimo de busqueda de camino distinto
#     Metodo ORB para capturar la posicion de la cabeza por caractisticas
#     Cambiar el juego interno
#     Aprendizaje por refuerzo
#     Con clock (x)
