import math
import heapq
from collections import defaultdict
from runprofiler import runprofiler

degreeMap = {
    0: [-3, 1],
    15: [-2, 1],
    30: [-1, 1],
    45: [-1, 2],
    60: [-1, 3],
    75: [0, 1],
    90: [1, 3],
    105: [1, 2],
    120: [1, 1],
    135: [2, 1],
    150: [3, 1],
    165: [1, 0],
}

def reconstruct_path(cameFrom, current):
    path = [current]

    while current.id in cameFrom:
        path = [current] + path
        current = cameFrom[current.id]

    return path

@runprofiler
def A_star(start, goal, obstacles, width=72, height=108):
    # G and H score dicts
    g = defaultdict(lambda: 10000000000000)
    f = defaultdict(lambda: 10000000000000)

    # Distance between nodes (manhattan dist. + angle diff)
    d = lambda n1, n2: abs(n2.y - n1.y) + abs(n2.x - n1.x) + abs(n2.a - n1.a)
    """ HEURISTIC
        * Far away from mining area = bad
        * Further away from the center (more likely to run into walls) = bad
        * Being turned (you have to turn back + move slower towards goal) = bad
    """
    def h(n):
        delta = degreeMap[n.a+75]
        return abs(n.y - goal.y) + 5 * abs(goal.x - n.x) + abs(n.a)

    class Node:
        def __init__(self, x, y, a):
            self.x = x
            self.y = y
            self.a = a
            self.id = self.x * height * 12 + self.y * 12 + ((self.a + 75) // 15)

        def get_neighbors(self):
            delta = degreeMap[self.a + 75]
            neighbors = []

            norm_a = self.a // 15
            # Move forward
            try:
                if self.x + delta[0] >= 0:
                    obs = obstacles[self.x + delta[0]][self.y + delta[1]][norm_a+5]
                    if not obs:
                        neighbors.append(Node(x = self.x + delta[0], y = self.y + delta[1], a = self.a))
            except:
                pass
            # Move backward
            try:
                if self.x - delta[0] >= 0 and self.y - delta[1] >= 0:
                    obs = obstacles[self.x - delta[0]][self.y - delta[1]][norm_a+5]
                    if not obs:
                        neighbors.append(Node(x = self.x - delta[0], y = self.y - delta[1], a = self.a))
            except:
                pass
            # Turn right
            try:
                obs = obstacles[self.x][self.y][norm_a+6]
                if not obs:
                    neighbors.append(Node(x = self.x, y = self.y, a = self.a + 15))
            except:
                pass
            # Turn left
            try:
                if norm_a + 4 >= 0:
                    obs = obstacles[self.x][self.y][norm_a+4]
                    if not obs:
                        neighbors.append(Node(x = self.x, y = self.y, a = self.a - 15))
            except:
                pass

            return neighbors#[n for n in neighbors if n.is_valid()]

        def is_valid(self):
            try:
                if self.x >= 0 and self.y >= 0 and self.a+75 >= 0:
                    obs = obstacles[self.x][self.y][(self.a+75)//15]
                    return not obs
                else:
                    return False
            except IndexError:
                return False
            # if self.x <= 0 or self.x >= width:
            #     return False
            # if self.y <= 0 or self.y >= height:
            #     return False
            # if self.a < -75 or self.a > 90:
            #     return False
            # return not obstacles[self.x][self.y][(self.a+75)//15]

        # Determines how priority queue sorts
        def __lt__(self, other):
            return f[self.id] < f[other.id]

        def __repr__(self):
            return f"({self.x}, {self.y})"

    start = Node(start.x, start.y, 0)

    g[start.id] = 0
    f[start.id] = h(start)

    openSet = [] # Priority Queue Heap
    ids = {}

    heapq.heappush(openSet, start)
    ids[start.id] = True

    cameFrom = {}

    while len(openSet) > 0:
        current = heapq.heappop(openSet)
        if current.id in ids:
            del ids[current.id]

        # End condition
        if current.y <= goal.y:
            return reconstruct_path(cameFrom, current)

        for neighbor in current.get_neighbors():
            tentative_gScore = g[current.id] + d(current, neighbor)
            if tentative_gScore < g[neighbor.id]:
                cameFrom[neighbor.id] = current
                g[neighbor.id] = tentative_gScore
                f[neighbor.id] = tentative_gScore + h(neighbor)
                if neighbor.id not in ids:
                    ids[neighbor.id] = True
                    heapq.heappush(openSet, neighbor)

    # No solution
    return []
