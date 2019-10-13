# Contains methods for the control and monitoring of various motors
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from pysabertooth import Sabertooth
import busio

#
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus, address=0x40)
pca.frequency = 1600

#
motor0 = Sabertooth(pca.channels[0], 0.1)
motor1 = Sabertooth(pca.channels[1], 0.1)
motor2 = Sabertooth(pca.channels[2], 0.1)
motor3 = Sabertooth(pca.channels[3], 0.1)

motor_speeds = [0, 0, 0, 0]
chassis_speed = 0


class motors:

    @staticmethod
    def set_motor_speed(motor, percent):
        if(motor == 0):
            motor0.drive(1, percent)
        elif(motor == 1):
            motor1.drive(1, percent)
        elif(motor == 2):
            motor2.drive(1, percent)
        elif(motor == 3):
            motor3.drive(1, percent)
        motor_speeds[motor] = percent

    @staticmethod
    def set_chassis_speed(percent):
        motor0.drive(1, percent)
        motor1.drive(1, percent)
        motor2.drive(1, percent)
        motor3.drive(1, percent)
        motor_speeds = [percent, percent, percent, percent]
        chassis_speed = percent

    @staticmethod
    def get_motor_speed(motor):
        return motor_speeds[motor]

    @staticmethod
    def get_chassis_speed():
        return chassis_speed

    @staticmethod
    def estop():
        motor0.stop()
        motor1.stop()
        motor2.stop()
        motor3.stop()
        motor_speeds = [0, 0, 0, 0]
        chassis_speed = 0

    @staticmethod
    def arcade_drive(throttle, turn):


    @staticmethod
    def tank_drive(left_percent, right_percent):
        motor0.drive(1, left_percent)
        motor1.drive(1, left_percent)
        motor2.drive(1, right_percent)
        motor3.drive(1, right_percent)
        motor_speeds = [left_percent, left_percent, right_percent, right_percent]
