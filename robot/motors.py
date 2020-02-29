# Contains methods for the control and monitoring of various motors
#from board import SCL, SDA
#from adafruit_pca9685 import PCA9685
from pysabertooth import Sabertooth
import busio
import ASUS.GPIO as GPIO
import time

# each Sabertooth controls 2 motors
l_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address = 128, timeout=1000)
r_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address = 129, timeout=1000)
TD_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address = 130, timeout=1000)


# Chassis motors
class DriveTrain:

    motor_speeds = [0, 0, 0, 0]

    ## Motor Numbers: (subject to change)
    # 0 - Front-Left
    # 1 - Back-Left
    # 2 - Front-Right
    # 3 - Back-Right


    # set speed for individual wheel [-100%,+100%]
    @staticmethod
    def set_motor_speed(motor, percent):
        print("set mot speed:", motor, percent)
        if motor == 0 or motor == 2 :
            l_saber.drive(0 if motor == 0 else 1, percent)
        elif motor == 1 or motor == 3:
            r_saber.drive(0 if motor == 1 else 1, percent)
        else:
            raise Exception("bad motor number")

        DriveTrain.motor_speeds[motor] = percent


    @staticmethod
    def stop():
        l_saber.stop()
        r_saber.stop()
        DriveTrain.motor_speeds = [0, 0, 0, 0]

    # both arguments are percents
    @staticmethod
    def arcade_drive(throttle, turn):
        v = (100 - abs(turn)) * (throttle / 100) + throttle
        w = (100 - abs(throttle)) * (turn / 100) + turn
        l = (v + w) / 2
        r = (v - w) / 2
        # send tank drive command
        DriveTrain.tank_drive(l, r)

    @staticmethod
    def tank_drive(left_percent, right_percent):
        DriveTrain.set_motor_speed(0, left_percent)
        DriveTrain.set_motor_speed(1, left_percent)
        DriveTrain.set_motor_speed(2, right_percent)
        DriveTrain.set_motor_speed(3, right_percent)
        motor_speeds = [ left_percent, left_percent, right_percent, right_percent ]

class Trenchdigger:
#    def servo(angle):
#        GPIO.setmode(GPIO.ASUS)
#        GPIO.setwarnings(False)
#
#        servo = 238
#
#    TD_speed = 0

    @staticmethod
    def set_TD_speed(percent):
        TD_saber.drive(0, percent)
        TD_speed = percent

    @staticmethod
    def TD_stop():
        TD_saber.drive(0, 0)
        TD_speed = 0
