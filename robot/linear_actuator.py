from simple_pid import PID


class DummyADC:
    def __init__(self):
        self.val = 0.6

    def get_value(self):
        return self.val


class LinearActuator:

    def __init__(self, adc: DummyADC, sabertooth, port_id):
        self.pos = adc.get_value()
        self.AD = adc
        self.st = sabertooth
        self.id = port_id

    def _balance(self):
        pid = PID(setpoint=self.pos, sample_time=0.01, output_limits=(-1, 1))
        # PID.sample_time = 0.01
        # PID.setpoint = adc
        # PID.output_limits = (-1, 1)
        while True:
            self.AD = pid.__call__(self.AD)


class LinearActuatorPair:

    def __init__(self, position, la1, la2):
        self.pos = position
        self.LinAc1 = la1
        self.LinAc2 = la2

    def set_position(self, la1, la2):
        self.pos = la1.pos




