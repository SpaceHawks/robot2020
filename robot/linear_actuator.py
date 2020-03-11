from simple_pid import PID
import threading

top_limit_switch = AnalogIn(5)
bottom_limit_switch = AnalogIn(6)
tls_value = None
bls_vlaue = None

class DummyADC:
    def __init__(self):
        self.val = 0.6

    def get_value(self):
        return self.val


class LinearActuator:

    def __init__(self, adc: DummyADC, sabertooth, port_id, constants=(5, 0.01, 0.1)):
        self.pos = adc.get_value()
        self.adc = adc
        self.st = sabertooth
        self.id = port_id
        self.estop = False

        kp, ki, kd = constants

        self.pid = PID(kp, ki, kd,
                       setpoint=self.adc.get_value(),
                       sample_time=0.02,
                       output_limits=(-1, 1))

        self.bal_thread = threading.Thread(target=self._balance, args=())
        self.bal_thread.daemon = True
        self.bal_thread.start()

    def read_limit_switches(opt):
        tls_value = top_limit_switch.value
        bls_vlaue = bottom_limit_switch.value
        if(opt == t):
            return tls_value
        if(opt == b):
            return bls_value


    def _balance(self):
        # PID.sample_time = 0.01
        # PID.setpoint = adc
        # PID.output_limits = (-1, 1)
        self.enable = False
        v = self.adc.get_value()
        while(self.estop == False):
            top = LinearActuator.read_limit_switches(t)
            bottom = LinearActuator.read_limit_switches(b)
            if(top == 1 || bottom == 1):
                self.enable = False
            elif(top == 0 && bottom == 0):
                self.enable = True
            if(self.enable):
                control = self.pid(v)
                self.st.drive(self.id, 100 * control)
                v = self.adc.get_value()
                sleep(0.01)

    def estop(self):
        self.estop = True

class Hopper:
    def __init__(self, position, la):
        self.pos = position
        self.la = la

    def set_hopper(self, pos):
        self.pos = pos
        self.la.pos = self.pos

class LinearActuatorPair:

    def __init__(self, position, la1, la2):
        self.pos = position
        self.la1 = la1
        self.la2 = la2
        #self.enable = False

    def set_position(self, pos):
        self.pos = pos
        self.la1.pos = self.pos
        self.la2.pos = self.pos
