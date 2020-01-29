import time
from generate_obstacles import generate_obstacles

start= time.time()
obstacles = generate_obstacles()
print(f"{time.time() - start} seconds to 3D-ize 50 obstacles")



width = 360
height = 540
slice = []
chosen_angle = -30 # Robot is turned 30 degrees northeast [-75, 90]
for x in range(width//5):
    for y in range(height//5):
        if obstacles[x][y][(chosen_angle+75)//15] is True:
            slice.append((x,y))

red = "\033[31m"
yellow = "\033[33m"
cyan = "\033[36m"
end = "\033[0m"

print(f"\n{yellow}{len(slice)}{red} grid points filled. Text file of coordinates outputted to {yellow}output.txt.{red} Use {cyan}http://www.shodor.org/interactivate/activities/OrderedSimplePlot/{red} to view a plot of them.\n{end}")
with open("output.txt", "w") as text_file:
    print(str(slice)[1:-1], file=text_file)
