# Contains methods for the control and monitoring of various motors
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import busio
class motors:

    @staticmethod
    def __inti__():
        i2c_bus = busio.I2C(SCL, SDA)
        pca = PCA9685(i2c_bus)

        motor_speeds = [0, 0, 0, 0]
        chassis_speed = 0

    @staticmethod
    def set_motor_speed(percent, channel):
        freq = (percent/100)*1600
        pca.channels[channel] = freq

    @staticmethod
    def set_chassis_speed():

    @staticmethod
    def get_motor_speed():

    @staticmethod
    def get_chassis_speed():

    @staticmethod
    def estop():

    @staticmethod
    def arcade_drive():

    @staticmethod
    def tank_drive():
