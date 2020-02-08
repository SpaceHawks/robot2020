from generate_obstacles import generate_obstacles
from a_star import A_star

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

start = Point(36, 90)
goal = Point(36, 10)

obs = generate_obstacles()
path = A_star(start, goal, obs)
print(path)
