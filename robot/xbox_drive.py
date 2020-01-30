import xbox
import time
import motors


joy = xbox.Joystick();
avg_x = 0
avg_y = 0

while True:
    x,y = joy.leftStick()
    x, y = x * 100, y * 100
    # exponential moving average to reduce brownout
    avg_x = (x + avg_x) / 2
    avg_y = (y + avg_y) / 2

    print({'x':x, 'y':y});
    motors.DriveTrain.arcade_drive(avg_y, avg_x)
    time.sleep(1 / 8)
