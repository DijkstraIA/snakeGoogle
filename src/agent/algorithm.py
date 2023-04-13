from numpy import sqrt
import numpy as np

from model.piece import node

#Variables auxiliares
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
dword = ['right', 'down', 'left', 'up']
dfsFlag = 0

class algorithms:
    def __init__(self):
        self.ini = 1

    def asterisk1(self, food1, snake1, grid, rows, cols):
        food1.camefrom = []
        for s in snake1:
            s.camefrom = []
        openset = [snake1[-1]]
        closedset = []
        dir_array1 = []
        while 1:
            current1 = min(openset, key=lambda x: x.f)
            openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
            closedset.append(current1)
            for neighbor in current1.neighbors:
                if neighbor not in closedset and neighbor not in snake1:
                    tempg = neighbor.g + 1
                    if neighbor in openset:
                        if tempg < neighbor.g:
                            neighbor.g = tempg
                    else:
                        neighbor.g = tempg
                        openset.append(neighbor)
                    neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.camefrom = current1
            if current1 == food1:
                break
        while current1.camefrom:
            if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
                dir_array1.append(2)
            elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
                dir_array1.append(0)
            elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(3)
            elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(1)
            current1 = current1.camefrom
        for i in range(rows):
            for j in range(cols):
                grid[i][j].camefrom = []
                grid[i][j].f = 0
                grid[i][j].h = 0
                grid[i][j].g = 0
        return dir_array1


    def bfs(self, food, snake, rows, cols):
        snake1 = np.array(snake)
        food1 = food

        dist = np.full((rows, cols), -1)
        pending = []
        direction = []

        pending.append(snake1[-1])
        for node in snake1:
            dist[node.x][node.y] = 0

        while len(pending) > 0:
            current = pending.pop(0)
            for neighbor in current.neighbors:
                if dist[neighbor.x][neighbor.y] == -1:
                    dist[neighbor.x][neighbor.y] = dist[current.x][current.y] + 1
                    pending.append(neighbor)
                    neighbor.camefrom = current
            if current == food1:
                break
        
        current = food1
        while current != snake1[-1]:
            diri = current.x - current.camefrom.x
            dirj = current.y - current.camefrom.y
            # print(["from",current.x, current.y])
            # print(["to",current.camefrom.x, current.camefrom.y])
            if diri == -1:
                direction.append(3)
            elif diri == 1:
                direction.append(1)
            elif dirj == 1:
                direction.append(0)
            elif dirj == -1:
                direction.append(2)
            current = current.camefrom

        # dword = ['right', 'down', 'left', 'up']    
        return direction

    def dfs(self, food, current, rows, cols, vis):
        global dfsFlag
        if dfsFlag == 1:
            return
        vis[current.x][current.y] = 0
        for neighbor in current.neighbors:
            if vis[neighbor.x][neighbor.y] == -1:
                self.dfs(food, neighbor, rows, cols, vis)
                neighbor.camefrom = current
        if current == food:
            dfsFlag = 1
            return
        


    def dfsAll(self, food, snake, rows, cols):
        snake1 = np.array(snake)
        food1 = food
        vis = np.full((rows, cols), -1)

        for node in snake1:
            vis[node.x][node.y] = 0
        
        global dfsFlag
        dfsFlag = 0
        self.dfs(food1, snake1[-1], rows, cols, vis)
        direction = []

        current = food1
        while current != snake1[-1]:
            diri = current.x - current.camefrom.x
            dirj = current.y - current.camefrom.y
            if diri == -1:
                direction.append(3)
            elif diri == 1:
                direction.append(1)
            elif dirj == 1:
                direction.append(0)
            elif dirj == -1:
                direction.append(2)
            current = current.camefrom

        # dword = ['right', 'down', 'left', 'up']    
        return direction