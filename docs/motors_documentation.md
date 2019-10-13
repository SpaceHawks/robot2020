
Documentation for the Motors Library (motors.py)

Methods:
1.) set_motor_speed(motor, percent)
    Sets a certain motor to a designated power percentage (speed)
    motor: ID number of motor to power (0-3)
    percent: The percent power to send to the motor (-1-1)

2.) set_chassis_speed(percent)
    Sets all motors to the same speed
    percent: The percent power to send to the motor (-1-1)

3.) get_motor_speed(motor)
    Returns the value in the motor_speeds[] list corresponding to the passed value
    motor: ID of the motor being checked (0-3)

4.) get_chassis_speed()
    Returns the value of chassis_speed

5.) estop()
    Sets all motor speed values to zero

6.) tank_drive(left_percent, right_percent)
    Sets the left and right motors to different speeds for driving/turning
    left_percent: the power percentage for the left two motors (-1-1)
    right_percent: the power percentage for the right two motors (-1-1)

7.) arcade_drive(throttle, turn)
    Controls the chassis based in a throttle and turn speed
    throttle: the speed to move the chassis forwards (-1-1)
    turn: the turn speed of the chassis (-1-1)
