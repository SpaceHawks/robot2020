import xbox
from motors import motors
import time

joy = xbox.Joystick()

while True:
    x, y = joy.leftStick()
    x, y = x * 100, y * 100
    motors.arcade_drive(y, x)

    #print("x:", x, "y: ", y)
    time.sleep(1)
