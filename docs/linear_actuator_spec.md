# linear actuators

## PID Controller Library
- find one for python online, should have plenty of options

## ADC dummy class 
- dummy class to simulate an adc so that we can measure the potentiometer
- constructor takes a port number as arguments
### methods
- constructor: takes a port number as argument
- `get_value`: 
  - simulates geting a float value from the adc
  - scaled from 0 - 1

## Linear Actuator Class
### attributes
- `position`: float from 0-1 where linear actuator should move to
- `adc`: ADC dummy class
- `st`: relevant `SaberTooth` object
- `id`: relevant device id for when we call `st.drive`

### methods
- constructor: 
  - on start, sets position to value from adc dummy class
  - calls `_balance` in new thread
- `_balance`:
  - move linear actuator to `position` using PID and `st.drive` (see `motors.py` for examples)

## Linear Actuator Pair Class
- class definition for two linear actuators that must be aligned to be the same height at all times
### attributes
- `_position`: where should they be aligned to
- relevant `LinearActuator` objects
### methods
- constructor: Takes two `LinearActuator` as arguments
  - sets `_position` = the position of the first `LinearActuator`
  - calls balance
- `balance`:
  - aligns the linear actuators so that both of their adcdummy values line up
  - if the `position` attribute is `None` align them both to the first one's current value
- `set_position`
  - update `_position`
  - call `balance`
  - need to make sure that while moving one doesn't get too far ahead of the other
    - likely will involve using a thread
