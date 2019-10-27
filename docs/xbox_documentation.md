Documentation for the Xbox Control Library (xbox.py)
# Methods:
- `__init__(self, refreshRate)`
    - Creates xbox controller object
    - Sets controller refresh rate
    - Checks if a valid xbox controller is connected
    - self: the controller object
    - refreshRate: the number of milliseconds* between each refresh of the controller
- `refresh(self)`
    - Refreshes the joystick based on refreshRate

- `connected(self)`
    - Returns the connection status of the xbox controller

- `leftX(self, deadzone)`
    - Reads and returns the value of the x-axis of the left joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `leftY(self, deadzone)`
    - Reads and returns the value of the y-axis of the left joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `rightX(self, deadzone)`
    - Reads and returns the value of the x-axis of the right joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `rightY(self, deadzone)`
    - Reads and returns the value of the y-axis of the right joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `leftStick(self, deadzone)`
    - Returns a combination of X and Y axis values for the left joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `rightStick(self, deadzone)`
    - Returns a combination of X and Y axis values for the right joystick
    - deadzone: the range of value for which there is no output (to reduce motor drift from imprecise joysticks)

- `Note: I have left out the button methods at this time because I am not sure which ones we are using. I will add them as we need them.`
