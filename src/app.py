from agent.agentSnake import IA

agent = IA()

def main():
    agent.playVirtual() # Simulacion sin lectura de sensores
    # agent.play() # Simulacion con lectura de sensores

if __name__ == "__main__":
    main()

# Path: agent\agentSnake.py

#Intentar que la cabeza se actualice con la posicion de la cabeza real