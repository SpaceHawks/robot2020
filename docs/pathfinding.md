# Pathfinding

## Purpose
To efficiently navigate through an unknown terrain of boulders and craters using a LIDAR sensor to detect them in advance, and an algorithm to avoid them once detected.

## Possibilities
Many different methods of avoiding these obstacles are available, but we need one that is efficient, easy to implement, and reliable. The obstacle data we receive restricts us in that:
- It is short ranged
- They are collected as individual points
- There will probably be many of them

These restrictions require an algorithm such that, upon receiving new obstacle points, the robot can quickly calculate how to avoid it (if it even needs to). 

So, instead of trying to calculate and continually modify a *path*, we will simply avoid any obstacles within some radius `r`. Some pseudocode for this might look like:
```py
    while robot in obstacle_area:
        if robot.near(obstacles):
            avoid(obstacles)
        else:
            go_forward()
```

In other words, if there's some obstacle(s) close by, angle the robot such that there won't be a collision, otherwise just drive forward (straight forward, not at the previous angle).

## Avoiding

So how should `avoid()` work? For every possible angle the robot could go (±180°), which one is:
1. The closest to the current angle (We want to turn for as short as possible)
2. The least likely to hit an obstacle (Obviously, we don't want to run into an obstacle)
3. The closest to straight forward (We will reach the goal faster)

\#1 and \#3 are easy, but #2 requires some thought.

How do we determine if the robot will hit an obstacle, given:
- θ: the angle the robot will travel at (-180°, 180°)
- (Ox, Oy): The x and y coordinates of an obstacle
- (x, y, w, h): The x and y coordinates, as well as the width and height, of the robot

It's actually not too hard! Using a bit of math, we can simply calculate the **perpindicular distance** from the line the robot would be travelling at (calculated using θ, x, and y) to the obstacle. If this distance is less than half the width of the robot, then the robot will collide. We can also add a small buffer here to be safe.

#### Line Equation
First, let's calculate the line the robot would be travelling at.

The standard equation of a line is:

>`y = m (x - x1) + y1`

We know what x1 and y1 are- they're just the robot's (Rx, Ry) coordinates. We have to use `θ` to find m. 

Our angle is (-180°, 180°). You can map this angle, `θ`, to the normal (0°, 360°), `θn`, by:

>`θn = (-θ+ 90) % 360`

Using this fact, and the fact that we can find `m` from any (0°, 360°) angle via:

>`m = tan(θn)`

We can then find `m` from any (-180°, 180°) angle using:

>`m = tan(-θ + 90)`

Note that there is no need for the `% 360` anymore, since `tan` "handles" that anyway.

We finally have the equation for the line!

>`y = tan(-θ + 90) * (x - Rx) + Ry`



#### Perpindicular distance
Let's write the previous line equation into the form `ax + by + c = 0`:

`-tan(-θ + 90)*x + y + (tan(-θ + 90)*Rx - Ry) = 0`

Now we can write the values of a, b, and c:

`a = -tan(-θ + 90)`<br>
`b = 1`<br>
`c = tan(-θ + 90) * Rx - Ry`

The equation for the perpindicular distance from a point (Ox, Oy) to a line `ax + by + c = 0` is:

![](http://www.sciweavers.org/tex2img.php?eq=%5Cfrac%7B%7CaO_x%2BbO_y%2Bc%7C%7D%7B%5Csqrt%7Ba%5E2%20%2B%20b%5E2%7D%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev)

Plugging in all relevant values and simplifying (a lot) gives the equation:

![Perpindicular distance equation](http://www.sciweavers.org/tex2img.php?eq=%7C(O_x-R_x)cos(%5Ctheta)%20%2B%20(O_y-R_y)sin(%5Ctheta)%7C&bc=White&fc=Black&im=jpg&fs=12&ff=arev)


A very nice formula. Note that this *still* uses `(-180°, 180°)` angles.

### Updated pseudocode
The simplest way to check for valid angles is:
```py
b = 0.1 # Buffer for avoiding obstacles
safe_dist = r.w / 2 + b
while r in obstacle_area:
    if r.near(obstacles):
        for a in range(-180, 180, 2): # Check every angle
            an = a * PI / 180
            ok = True
            for o in obstacles: # Check every obstacle
                if abs((o.x - o.y) * cos(an) - (o.y - r.y) * sin(an)) <= safe_dist:
                    # invalid angle
                    ok = False
                    break
            if (ok):
                #valid angle - how do we decide which one to choose?
                pass
    else:
        go_forward()
```
But how efficient is this? The outer `for` loop (angles) always runs **180** times. The inner loop will run for however many obstacle points there are, until an obstacle will be collided with. Let's say there are **100**. This means it could run the perpindicular distance calculation **18,000** times. Yikes. We can use our other two criteria to allow us to not check as many angles and exit the loop(s) way before we get to 18,000.

A much better approach would be:
```py
b = 0.1  # Buffer for avoiding obstacles
safe_dist = r.w / 2 + b

a_s = 1.5  # angle step
angles = [(0.5 * a_s * a if a % 2 == 0 else - a_s * 0.5 * (a + 1)) for a in range(0, int(360 / a_s))]
# Produces [0, -1.5, 1.5, -3, 3, ...]

while r in obstacle_area:
    if r.near(obstacles):
        best_angle = 0
        for a in angles:  # Check every angle
            an = (a + r.a) * PI / 180  # 1 - Searches angles near current angle first
            if (path_clear(an)):
                best_angle = an
                break
        turn_to_angle(best_angle)
    else:
        # 3 - Go straight forward if possible
        go_forward()


def path_clear(an):
    # 2 - Don't hit an obstacle
    valid = True
    for o in obstacles:  # Check every obstacle
        if abs((o.x - o.y) * cos(an) - (o.y - r.y) * sin(an)) <= safe_dist:
            valid = False
            break
    return valid
```

Now how efficient? Well, we now first check if the angles around the current angle are still valid - most of the time this will be true. This significantly reduces the number of checks we have to make on average. 

This also now meets all three of our criteria - it first tries angles close to the current one, then at least finds an angle which has no collisions, and finally if it is far enough away from obstacles, it will go forward.

#### A slight issue
An issue you may have noticed is in how collisions are checked for. Remember, we are basically drawing a line along which the robot will travel, and then checking the perpindicular distance to each obstacle. The issue is that **the line extends in both directions**.

Imagine the following scenario:
![The issue](https://i.imgur.com/1KvgIjk.png)

Obviously, the robot will detect that if it takes the dotted path, it will run into B. It should just slightly adjust its path to the left, right? 

No.

If A turns left more, the path line will still be colliding with ***A***. It will turn much more drastically than necessary in order to avoid something it never was going to hit. 

How can we fix this? The line should obviously start at (Rx, Ry) and project only forward, not backwards, but there's no way to extract this information from the perpindicular formula, so another, separate check must be added.

One way to determine if the robot is moving *towards* an obstacle would be to say that the distance from the robot to the obstacle a split second later along the path should be less than the current distance.

Let P equal the point along the path n units later. The equation for Px and Py would be:

`Px = Rx + n`<br>
`Py = Ry + n*cot(θ)`

Therefore, `dist(P, O) > dist(R, O)` would imply the robot is moving *away* from the obstacle. Plug in these values to the distance formula, simplify (assume `n->0+`), and you get:

`sin(θ)*(Ox-Rx) + cos(θ)*(Oy-Ry) < 0`, **invalid obstacle/moving away from it.**

> Note that the x's are paired with sin(θ) instead of cos(θ) because of the (-180°, 180°) angles.

We simply now modify the `path_clear()` method to reflect this change:
```py
def path_clear(an):
    # 2 - Don't hit an obstacle
    valid = True
    for o in obstacles:  # Check every obstacle
        dx = o.x - r.x
        dy = o.y - r.y
        ca = cos(an)
        sa = sin(an)
        if (abs(dx * ca - dy * sa) <= safe_dist and (-ca * dy < sa * dx))::
            valid = False
            break
    return valid
```

Every piece is now in place- we can find the optimal angle which is closest to our current angle, not running into any obstacles, and ultimately moving towards the mining area.

Some example code is as follows:
<details><summary>Code for testing Avoid class</summary>
<p>

```python
from pathfinding import Avoid
import math
import random
import time


class Robot:
    def __init__(self, x, y, w, h, a=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.a = a


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Obstacle: (" + str(self.x) + ", " + str(self.y) + ")"


R = Robot(10, 10, 2, 2, 0)

avoid = Avoid(R.w, R.h, 1.0, 0.1, 25)

start = time.time()

# How long to get the angle 1000 times in a row with 1000 obstacles?
for i in range(1000):
    obstacles = []
    for _ in range(1000):
        obstacles.append(Obstacle(random.uniform(R.x - 20, R.x + 20), random.uniform(R.y - 20, R.y + 20)))

    a = avoid.get_angle(R, obstacles)
    R.x += random.uniform(-2, 2)
    R.y += random.uniform(-2, 2)

total_time = time.time() - start
# On Raspberry Pi 3B+, angles/second ~= 30,000 / # of obstacles
print(str(total_time / 1000) + " seconds/angle", str(1000 / total_time) + " angles/second")


```

</p>
</details>

### Performance
This code was tested on a Raspberry Pi 3B+ (less powerful than the robot's Tinkerboard) and was able to calculate about `30,000 / n` angles per second, where n is the number of obstacle points. This means if there are 1,000 obstacle points, we can update our trajectory approximately 30 times per second. This also means that the calculation time scales pretty much *linearly* as the number of obstacle points grows.
