from numpy import sqrt
import numpy as np
import heapq

#Variables auxiliares
dfsFlag = 0

class algorithms:

    def bfs(self, food, snake, rows, cols):
        snake1 = np.array(snake)
        food1 = food

        dist = np.full((rows, cols), -1)
        pending = []

        for node in snake1:
            dist[node.x][node.y] = 0

        pending.append(snake1[-1])
        dist[food1.x][food1.y] = -1

        while len(pending) > 0:
            current = pending.pop(0)
            for neighbor in current.neighbors:
                if dist[neighbor.x][neighbor.y] == -1:
                    dist[neighbor.x][neighbor.y] = dist[current.x][current.y] + 1
                    pending.append(neighbor)
                    neighbor.camefrom = current
            if current == food1:
                break
        if dist[food1.x][food1.y] == -1:
            return []           
        return self.path(food1, snake1[-1])
    
    def asterisk(self, food, snake, rows, cols):
        snake1 = np.array(snake)
        food1 = food

        oo = 1000000
        cola_prioridad = []
        processed = np.full((rows, cols), 0)
        distance = np.full((rows, cols), oo)

        for node in snake1:
            processed[node.x][node.y] = 1                
        
        snake1[-1].g = 0
        snake1[-1].h = abs(snake1[-1].x - food1.x) + abs(snake1[-1].y - food1.y)
        snake1[-1].f = snake1[-1].g + snake1[-1].h

        distance[snake1[-1].x][snake1[-1].y] = 0
        processed[food1.x][food1.y] = 0
        processed[snake1[-1].x][snake1[-1].y] = 0
        heapq.heappush(cola_prioridad, (0, snake1[-1]))

        itr = 0
        
        while len(cola_prioridad) > 0:
            current = heapq.heappop(cola_prioridad)[1]
            itr += 1
            if(processed[current.x][current.y] == 1):
                continue
            
            processed[current.x][current.y] = 1
            for neighbor in current.neighbors:
                w = self.f(current, neighbor, food1)
                if distance[current.x][current.y] + w < distance[neighbor.x][neighbor.y]:
                    distance[neighbor.x][neighbor.y] = distance[current.x][current.y] + w
                    heapq.heappush(cola_prioridad, (distance[neighbor.x][neighbor.y], neighbor))
                    neighbor.camefrom = current
            if current == food1:
                break

        if distance[food1.x][food1.y] == oo:
            return []
        return self.path(food1, snake1[-1])

    def f(self, current, neighbor, food):
        neighbor.g = 1 + current.g
        neighbor.h = abs(neighbor.x - food.x) + abs(neighbor.y - food.y)
        neighbor.f = neighbor.g + neighbor.h
        return neighbor.f

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
        vis[food1.x][food1.y] = -1
        self.dfs(food1, snake1[-1], rows, cols, vis)

        if vis[food1.x][food1.y] == -1:
            return []
        return self.path(food1, snake1[-1])

    def path(self, food, head):
        direction = []
        current = food
        while current != head:
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
        return direction