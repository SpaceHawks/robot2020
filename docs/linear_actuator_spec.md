# linear actuators

## PID Controller Library
- find one for python online, should have plenty of options

## ADC dummy class 
- dummy class to simulate an adc so that we can measure the potentiometer
- constructor takes a port number as arguments
- methods: 
  - getValue(): gets float value scaled from 0 - 1 


## Linear Actuator Pair Class
- class definition for two linear actuators that must be aligned to be the same height at all times

- attributes:
  - `position`: float from 0 to 1 where linear actuators should move to
    - on startup this is set to `None`
- methods:
  - constructor:
    - constructor takes a `Sabertooth` object and 2x `ADC dummy class` as arguments
    - on start it calls the `_balance` method in a new thread
  - `_balance`:
    - aligns the linear actuators so that both of their adcdummy values line up
    - if the `position` attribute is `None` align them both to the first one's current value
    - use the pid controller to keep them balanced
