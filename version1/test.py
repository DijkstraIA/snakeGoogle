import cv2
import mss
import numpy as np
import pyautogui
import keyboard

dim_board = {
        'left': 35,
        'top': 212,
        'width': 680,
        'height': 610
    }

# Carga una imagen de muestra del juego Snake Arcade
# board =  sct.grab(monitor=dim_board)
# board = np.array(board)
path = "C:/Users/sebas/OneDrive/Escritorio/Inteligentes/snakeGoogle/version1"
dir = f"{path}/snake_arcade.png"
pyautogui.PAUSE = 0

ini = "s"
end = "q"
print("Press " + ini +" to start playing.")
print("Once started press " +  end + " to quit.")
keyboard.wait(ini)

while True:

    sct = mss.mss()
    img =  np.array(sct.grab(monitor=dim_board))

    # img = cv2.imread(board)

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica una umbralización para detectar los píxeles blancos
    ret, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # Encuentra los contornos de los objetos en la imagen
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Dibuja los contornos detectados en la imagen original
    cv2.drawContours(img, contours, -1, (0, 0, 255), 2)

    # ## Codigo para capturar los pixeles blancos
    # # Crear una máscara que contenga solo los píxeles blancos
    # lower_white = np.array([200, 200, 200])
    # upper_white = np.array([255, 255, 255])
    # print(len(lower_white))
    # print(len(upper_white))
    # mask = cv2.inRange(img, lower_white, upper_white)

    # # Encontrar las coordenadas de los píxeles no cero en la máscara
    # white_pixels = cv2.findNonZero(mask)

    # # Mostrar las coordenadas de los píxeles blancos en la imagen
    # print(white_pixels)
    # ## ------------------------------

    # Muestra la imagen resultante
    cv2.imshow("Imagen con contornos", img)
    cv2.waitKey(1)
    if keyboard.is_pressed(end):
        break
    # cv2.destroyAllWindows()

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
    