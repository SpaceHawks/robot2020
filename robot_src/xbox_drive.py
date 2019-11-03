import xbox
import motors
import time

joy = xbox.Joystick()

while True:
    x, y = joy.leftStick()
    motors.arcade_drive(y, x)
    time.sleep(1 / 16)
