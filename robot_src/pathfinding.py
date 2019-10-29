import math


class Avoid:
    def __init__(self, w=0.5, l=1.0, a_s=1.0, b=0.1, avoid_radius=10):
        self.b = 0.1  # Buffer for avoiding obstacles
        self.safe_dist = w / 2 + b
        self.angles = [(math.radians(0.5 * a_s * a) if a % 2 == 0 else math.radians(-a_s * 0.5 * (a + 1))) for a in range(0, int(360 / a_s))]
        self.dist_squared = avoid_radius ** 2

    def get_path_dir(self, robot, obstacles=[]):
        angle = self.get_angle(R, obstacles)
        if (abs(R.a - angle) < 3):  # Some small angle buffer to account for error
            return "forward"
        elif (R.a > angle):
            return "left"
        else:
            return "right"

    def get_angle(self, R, obstacles):
        best_angle = 0
        # Filter obstacles that are too far away to matter
        valid_obstacles = [(o, o.x - R.x, o.y - R.y) for o in obstacles]
        valid_obstacles = [o for o in valid_obstacles if self.dist_squared < o[1] ** 2 + o[2] ** 2]

        # Prefer current angle
        if self._path_clear(R, valid_obstacles, R.a):
            best_angle = R.a
        else:  # Otherwise find angle closest to 0 degrees (straight ahead)
            for a in self.angles:
                # an = (a + R.a)
                if self._path_clear(R, valid_obstacles, a):
                    best_angle = an
                    break
        return best_angle

    def _path_clear(self, R, obstacles, an):
        valid = True
        for O in obstacles:
            _, dx, dy = O
            ca = math.cos(an)
            sa = math.sin(an)
            if (abs(dx * ca - dy * sa) <= self.safe_dist and (-ca * dy < sa * dx)):
                valid = False
                break
        return valid

# For after the first traversal through the obstacles
class Pathfind:
    def __init__(self):
        pass
