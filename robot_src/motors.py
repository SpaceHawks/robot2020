# Contains methods for the control and monitoring of various motors
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor
import busio
class motors:

    @staticmethod
    def __inti__():
        i2c_bus = busio.I2C(SCL, SDA)
        pca = PCA9685(i2c_bus, address=0x60)
        pca.frequency = 1600

        channel0 = pca.channels[0]
        channel1 = pca.channels[1]

        channel2 = pca.channels[2]
        channel3 = pca.channels[3]

        channel4 = pca.channels[4]
        channel5 = pca.channels[5]

        channel6 = pca.channels[6]
        channel7 = pca.channels[7]

        motor0 = motor.DCMotor(channel0, channel1)
        motor1 = motor.DCMotor(channel2, channel3)
        motor2 = motor.DCMotor(channel4, channel5)
        motor3 = motor.DCMotor(channel6, channel7)

        motor_speeds = [0, 0, 0, 0]
        chassis_speed = 0

    @staticmethod
    def set_motor_speed(motor, percent):
        if(motor == 0):
            motor0.throttle = percent/100
        elif(motor == 1):
            motor1.throttle = percent/100
        elif(motor == 2):
            motor2.throttle = percent/100
        elif(motor == 3):
            motor3.throttle = percent/100
        motor_speeds[motor] = percent

    @staticmethod
    def set_chassis_speed(percent):
        motor0.throttle = percent/100
        motor1.throttle = percent/100
        motor2.throttle = percent/100
        motor3.throttle = percent/100
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
        motor0.throttle = 0
        motor1.throttle = 0
        motor2.throttle = 0
        motor3.throttle = 0
        motor_speeds = [0, 0, 0, 0]
        chassis_speed = 0

    @staticmethod
    def arcade_drive():

    @staticmethod
    def tank_drive(left_percent, right_percent):
        motor0.throttle = left_percent
        motor1.throttle = left_percent
        motor2.throttle = right_percent
        motor3.throttle = right_percent
        motor_speeds = [left_percent, left_percent, right_percent, right_percent]
