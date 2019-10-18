
Documentation for the Motors Library (motors.py)

# Methods:
- `set_motor_speed(motor, percent)`
    - Sets a certain motor to a designated power percentage (speed)
    - motor: ID number of motor to power (0-3)
    - percent: The percent power to send to the motor [-1,1]

- `set_chassis_speed(percent)`
    - Sets all motors to the same speed
    - percent: The percent power to send to the motor (-1-1)

- `get_motor_speed(motor)`
    - Returns the value in the motor_speeds[] list corresponding to the passed value
    - motor: ID of the motor being checked (0-3)

- `get_chassis_speed()`
    - Returns the value of chassis_speed

- `estop()`
    - Sets all motor speed values to zero

- `tank_drive(left_percent, right_percent)`
    - Sets the left and right motors to different speeds for driving/turning
    - left_percent: the power percentage for the left two motors (-1-1)
    - right_percent: the power percentage for the right two motors (-1-1)

- `arcade_drive(throttle, turn)`
    - Controls the chassis based in a throttle and turn speed
    - throttle: the speed to move the chassis forwards [-1, 1]
    - turn: the turn speed of the chassis [-1, 1]
