import math
from collections import defaultdict

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

def A_star(start, goal, obstacles):
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

        def get_neighbors():
            delta = degreeMap[this.a + 75]
            neighbors = []
            # Move forward
            neighbors.append(Node(x = self.x + delta[0], y = self.y + delta[1], a = self.a))
            # Move backward
            neighbors.append(Node(x = self.x - delta[0], y = self.y - delta[1], a = self.a))
            # Turn right
            neighbors.append(Node(x = self.x, y = self.y, a = self.a + 15))
            # Turn left
            neighbors.append(Node(x = self.x, y = self.y, a = self.a - 15))

            return [n for n in neighbors if n.isValid()]

        def isValid():
            if self.x <= 0 or self.x >= width:
                return False
            if self.y <= 0 or self.y >= height:
                return False
            if self.a < -75 or self.a > 90:
                return False
            return not obstacles[self.x][self.y][self.a+75]


    g = defaultdict(lambda: math.inf)
    f = defaultdict(lambda: math.inf)

    start = Node(start.x, start.y, 0)

    g[start.id] = 0
    f[start.id] = h(start)
