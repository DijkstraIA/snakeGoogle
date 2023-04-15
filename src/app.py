from agent.agentSnake import IA
import keyboard
from time import sleep

agent = IA()

def main():
    itr = 1
    while(True):
        print("Inicio de iteracion: ", itr)
        # agent.playVirtual() # Simulacion sin lectura de sensores
        agent.play() # Simulacion con lectura de sensores
        agent.reset()
        print("------------------")
        itr+=1
        sleep(.10)
        if keyboard.is_pressed("q") | itr > 10:
            break

if __name__ == "__main__":
    main()

# Path: agent\agentSnake.py

#Intentar
# 
#  que la cabeza se actualice con la posicion de la cabeza real