from simple_pid import PID


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
        
        kp, ki, kd = constants
        
        self.pid = PID(kp, ki, kd, 
                       setpoint=self.adc.get_value, 
                       sample_time=0.01, 
                       output_limits=(-1, 1))
        
        self.bal_thread = Thread(target=self._balance, args=())
        self.bal_thread.daemon = True
        self.bal_thread.start()

    def _balance(self):
        # PID.sample_time = 0.01
        # PID.setpoint = adc
        # PID.output_limits = (-1, 1)
        v = self.pid.update(0)
        while True:
            control = self.pid(v)
            v = self.pid.update(control)
                   
           
class LinearActuatorPair:

    def __init__(self, position, la1, la2):
        self.pos = position
        self.la1 = la1
        self.la2 = la2

    def set_position(self, pos):
        self.pos = pos
        self.la1.pos = self.pos
        self.la2.pos = self.pos
