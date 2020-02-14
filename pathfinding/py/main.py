import matplotlib.pyplot as plt
import time, math
from generate_obstacles import generate_obstacles
from a_star import A_star

# False = average run time, True = show plot
mode = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

start = Point(36, 90)
goal = Point(36, 10)

if mode:
    obs = generate_obstacles()
    path = A_star(start, goal, obs)

    obs_x = []
    obs_y = []

    for x in range(len(obs)):
        for y in range(len(obs[x])):
            if obs[x][y][0]:
                obs_x.append(x)
                obs_y.append(y)

    path_x = [p.x for p in path]
    path_y = [p.y for p in path]


    print(path_x, path_y)
    plt.plot(path_x, path_y, 'o', color="blue")
    plt.plot(obs_x, obs_y, 'o', color="green")
    plt.show()

else:
    total = 0
    max_val = 0
    for i in range(1000):
        obs = generate_obstacles()

        # Run and calculate time
        start_time = time.process_time()
        path = A_star(start, goal, obs)
        time_taken = time.process_time() - start_time

        total+=time_taken
        max_val = max(time_taken, max_val)

        print(f"PATH #{i+1}: {time_taken}\n{total/(i+1)} AVG\n\n")
        time.sleep(0.5)
