# Contains methods for the control and monitoring of various motors
#from board import SCL, SDA
#from adafruit_pca9685 import PCA9685
from pysabertooth import Sabertooth
import busio

#
#i2c_bus = busio.I2C(SCL, SDA)
#pca = PCA9685(i2c_bus, address=0x40)
#pca.frequency = 1600

#

l_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address = 128, timeout=1000)
r_saber = Sabertooth('/dev/ttyS1', baudrate=9600, address = 129, timeout=1000)

'''
motor0 = Sabertooth(pca.channels[0], 0.1)
motor1 = Sabertooth(pca.channels[1], 0.1)
motor2 = Sabertooth(pca.channels[2], 0.1)
motor3 = Sabertooth(pca.channels[3], 0.1)
'''

motor_speeds = [0, 0, 0, 0]
chassis_speed = 0


class motors:

    @staticmethod
    def set_motor_speed(motor, percent):
        print("set mot speed:", motor, percent)
        if motor == 0 or motor == 2 :
            l_saber.drive(0 if motor == 0 else 1, percent)
        elif motor == 1 or motor == 3:
            r_saber.drive(0 if motor == 1 else 1, percent)
        else:
            raise Exception("bad motor number")

    @staticmethod
    def set_chassis_speed(percent):
        pass #motor0.drive(1, percent)
        #motor1.drive(1, percent)
        #motor2.drive(1, percent)
        #motor3.drive(1, percent)
        #motor_speeds = [percent, percent, percent, percent]
        #chassis_speed = percent

    @staticmethod
    def get_motor_speed(motor):
        return motor_speeds[motor]

    @staticmethod
    def get_chassis_speed():
        return chassis_speed

    @staticmethod
    def estop():
        #motor0.stop()
        #motor1.stop()
        #motor2.stop()
        #motor3.stop()
        saber.stop()
        motor_speeds = [0, 0, 0, 0]
        chassis_speed = 0

    @staticmethod
    def arcade_drive(throttle, turn):
        v = (100 - abs(turn)) * (throttle / 100) + throttle
        w = (100 - abs(throttle)) * (turn / 100) + turn
        l = (v + w) / 2
        r = (v - w) / 2
        # send tank drive command
        motors.tank_drive(l, r)


    @staticmethod
    def tank_drive(left_percent, right_percent):
        '''
        motor0.drive(1, left_percent)
        motor1.drive(1, left_percent)
        motor2.drive(1, right_percent)
        motor3.drive(1, right_percent)
        '''
        motors.set_motor_speed(0, left_percent)
        motors.set_motor_speed(1, left_percent)
        motors.set_motor_speed(2, right_percent)
        motors.set_motor_speed(3, right_percent)
        motor_speeds = [left_percent, left_percent, right_percent, right_percent]
