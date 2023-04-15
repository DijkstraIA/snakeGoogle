from agent.agentSnake import IA
import time
import sys

agent = IA()
tiempo_inicio = time.time()
tiempo_limite = 65  # segundos

def main():
    itr = 1
    while(True):
        print("-+-+-Inicio de iteracion: ", itr)
        # agent.playVirtual() # Simulacion sin lectura de sensores
        agent.play() # Simulacion con lectura de sensores
        agent.reset()
        itr += 1
        tiempo_actual = time.time()
        if tiempo_actual - tiempo_inicio >= tiempo_limite:
            # Si ha pasado un minuto, detener el programa
            sys.exit()

if __name__ == "__main__":
    main()

# Path: agent\agentSnake.py

#Intentar
# 
#  que la cabeza se actualice con la posicion de la cabeza real