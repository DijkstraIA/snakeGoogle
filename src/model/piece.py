from pygame import draw, init
import numpy as np

dx = np.array([0, 1, 0, -1])
dy = np.array([1, 0, -1, 0])

class node:
    def __init__(self, x, y):
        self.x = x # Posicion en filas
        self.y = y # Posicion en columnas
        self.neighbors = []
        self.camefrom = []
        init()

        # Auxiliary variables for A*
        self.f = 0
        self.h = 0
        self.g = 0

    def show(self, color, screen, hr, wr):
        draw.rect(screen, color, [self.y*wr+2, self.x*hr+2, hr-4, wr-4])

    def inGrid(self, i, j, rows, cols):
        return i >= 0 and i < rows and j >= 0 and j < cols

    def add_neighbors(self, grid, rows, cols):
        for dir in range(4):
            if self.inGrid(self.x+dx[dir], self.y+dy[dir], rows, cols):
                self.neighbors.append(grid[self.x+dx[dir]][self.y+dy[dir]])
    
    # def __eq__(self, node2):
    #     return self.f == node2.f
    
    def __lt__(self, node2):
        return self.f < node2.f