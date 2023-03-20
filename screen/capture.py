import keyboard
import mss
import cv2
import numpy as np
from time import time, sleep
import pyautogui

w, h = pyautogui.size()
print("PIL Screen Capture Speed Test")
print("Screen Resolution: " + str(w) + 'x' + str(h))

pyautogui.PAUSE = 0
ini = "s"
end = "q"
print("Press " + ini +" to start playing.")
print("Once started press " +  end + " to quit.")
keyboard.wait(ini)


sct = mss.mss()
dim_board = {
        'left': 35,
        'top': 212,
        'width': 680,
        'height': 610
    }

w = 20 #38
h = 20 #50
dim_apple = {
        'left': 527, #515,
        'top': 505, #483,
        'width': w,
        'height': h
    }

apple =  np.array(sct.grab(monitor=dim_apple))#cv2.imread('apple.jpg')
#apple = cv2.cvtColor(apple, cv2.COLOR_RGB2BGR)

fps_time = time()
while True:
    board =  sct.grab(monitor=dim_board)
    board = np.array(board)
    #board = cv2.cvtColor(board, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR color
    
    #small = cv2.resize(board, (0, 0), fx=0.5, fy=0.5)
    #cv2.imshow("Computer Vision", small)
    

    #Procesar
    result = cv2.matchTemplate(board, apple, cv2.TM_CCOEFF_NORMED)
    cv2.imshow("Computer result", result)
    #_, max_val, _, max_loc = cv2.minMaxLoc(result)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > .85:
        print(f"Max Val: {max_val} Max Loc: {max_loc}")
        cv2.rectangle(board, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

    small = cv2.resize(board, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("Computer Vision", small)
    cv2.waitKey(1)
    #pyautogui.press("")
    #sleep(.10) # Comentar para mas fps
    if keyboard.is_pressed(end):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()