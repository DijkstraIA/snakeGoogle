import keyboard
import mss
import cv2
import numpy as np
from time import time, sleep
import pyautogui

# Variables
#Resolution
w, h = pyautogui.size()

#Input
ini = "s"
end = "q"

#Calculo casilla
eps = 3
disSquard = 40
iniX = 12
iniY = 10

wapple = 20 #38
happle = 20 #50

print("PIL Screen Capture Speed Test")
print("Screen Resolution: " + str(w) + 'x' + str(h))

print("Press " + ini +" to start playing.")
print("Once started press " +  end + " to quit.")
keyboard.wait(ini)
pyautogui.PAUSE = 0

dim_board = {
        'left': 35,
        'top': 212,
        'width': 680,
        'height': 610
    }

# dim_apple = {
#         'left': 527, #515,
#         'top': 505, #483,
#         'width': wapple,
#         'height': happle
# }

wapple = 680
happle = 610
dim_apple = {
        'left': 35, #515,
        'top': 212, #483,
        'width': wapple,
        'height': happle
}


sct = mss.mss()
apple =  np.array(sct.grab(monitor=dim_apple))#cv2.imread('apple.jpg')
#apple = cv2.cvtColor(apple, cv2.COLOR_RGB2BGR)

from pygame import time as time2

clock = time2.Clock()

fps_time = time()
cnt = 0
while True:
    # sleep(.1000)
    clock.tick(6)
    print(cnt)
    cnt+=1
    board =  sct.grab(monitor=dim_board)
    board = np.array(board)
    #board = cv2.cvtColor(board, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR color
    
    ap = cv2.resize(apple, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("Computer object", ap)
    
    #Procesar
    result = cv2.matchTemplate(board, apple, cv2.TM_CCOEFF_NORMED)
    cv2.imshow("Computer result", result)
    # _, max_val, _, max_loc = cv2.minMaxLoc(result)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > .75:
        print(f"Max Val: {max_val} Max Loc: {max_loc[0]} Max Loc: {max_loc[1]}")
        i = int((max_loc[1] - iniY) / disSquard) + 1
        j = int((max_loc[0] - iniX) / disSquard) + 1
        print([i,j])
        cv2.rectangle(board, max_loc, (max_loc[0] + wapple, max_loc[1] + happle), (0,255,255), 2)

    threshold = .95
    yloc, xloc = np.where(result >= threshold)
    print(len(xloc))
    # if len(xloc) == 0:
    #     break
    for(x,y) in zip(xloc, yloc):
        cv2.rectangle(board, (x,y), (x + wapple, y + happle), (0,255,255), 2)

    small = cv2.resize(board, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("Computer Vision", small)
    cv2.waitKey(1)
    pyautogui.press("")
    sleep(.10) # Comentar para mas fps
    if keyboard.is_pressed(end):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()


# import pyautogui

# while True:
#     print(pyautogui.position())