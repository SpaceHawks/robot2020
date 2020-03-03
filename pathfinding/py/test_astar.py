import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time, math
from generate_obstacles import generate_obstacles
from a_star import A_star
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--avg', action="store_true", help="Shows avg instead of plot")
parser.add_argument('-w', '--waypoints', action="store_true", help="Only shows waypoints")
args=parser.parse_args()

# False = average run time, True = show plot
show_plot = not args.avg

# Only show points in which the robot turns, not every point along the path
waypoints = args.waypoints

# How many cm x cm?
grid_size = 5

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

start = Point(180 // grid_size, 100 // grid_size)
goal = Point(180 // grid_size, 450 // grid_size)

def get_obs(obs, angle_drawn):
    obs_x = []
    obs_y = []

    for x in range(len(obs)):
        for y in range(len(obs[x])):
            if obs[x][y][10-angle_drawn]:
                obs_x.append(x)
                obs_y.append(y)



    return (obs_x, obs_y)

def get_path(path):
    path_x = []
    path_y = []
    prev_ang = None
    for p in path:
        if not waypoints or prev_ang == None or p.a != prev_ang:
            prev_ang = p.a
            path_x.append(p.x)
            path_y.append(p.y)

    path_x.append(path[-1].x)
    path_y.append(path[-1].y)
    return (path_x, path_y)
if show_plot:
    obs = generate_obstacles()
    path = A_star(start, goal, obs, width=360//grid_size, height=540//grid_size, grid_size=grid_size)
    (path_x, path_y) = get_path(path)
    (obs_x, obs_y) = get_obs(obs, 75//15)


    fig, ax = plt.subplots(figsize=(5.4, 8.1))
    plt.subplots_adjust(left=0.1, bottom=0.35)
    p_obs, = plt.plot(obs_x, obs_y, 'o', color="green")
    p_path, = plt.plot(path_x, path_y, 'o', color="blue")
    plt.plot([start.x, goal.x], [start.y, goal.y], 'o', color="red")
    plt.axis([0, 360//grid_size, 0, 540//grid_size])

    ax_slider = plt.axes([0.1, 0.2, 0.8, 0.05])
    slider = Slider(ax_slider, "Angle", valmin=-75, valmax=90, valinit=0, valstep=15, valfmt="%d°")

    button_slider = plt.axes([0.1, 0.1, 0.1, 0.05])
    new_map = Button(button_slider, 'Regenerate')

    def gen_new_map(val):
        # Make new obstacles
        global obs, obs_x, obs_y, path, path_x, path_y, slider
        obs = generate_obstacles()

        path = A_star(start, goal, obs, width=360//grid_size, height=540//grid_size, grid_size=grid_size)
        (path_x, path_y) = get_path(path)
        (obs_x, obs_y) = get_obs(obs, 75//15)

        p_obs.set_data(obs_x, obs_y)
        p_path.set_data(path_x, path_y)
        slider.set_val(0)
        plt.draw()

    def update_obs(an):
        (obs_x, obs_y) = get_obs(obs, int(an+75)//15)
        p_obs.set_data(obs_x, obs_y)
        plt.draw()

    new_map.on_clicked(gen_new_map)
    slider.on_changed(update_obs)
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
