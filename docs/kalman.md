# KalmanFilter

## Purpose
Combine readings from the IMU with the readings from the LIDAR to more accurately predect the robot's coordinates

### State Matrix
The state matrix is the current [`x`, `y`, `θ`, `x'`, `y'`, `ω`] of the robot. 
> This is the x y, and θ positions relative to what the LIDAR considers (0, 0, 0), along with the derivatives of these.

### Measurement
The measurement matrix is the observed [`x`, `y`, `θ`] of the robot. These values come from the LIDAR.
> Note that we aren't measuring every value in the state- this is perfectly fine!

## Example Usage
```py
from kalman import KalmanFilter
import numpy
import random
import json

# dt is how often measurement updates are done (dt=0.5s would imply a measurement every 0.5s)
# State Matrix contains the starting values [x, y, theta, x', y', w]
# Q and R are process and measurement error values, they need to be determined
kf = KalmanFilter(dt=1, stateMatrix=[23, 39, 0, 0, 0, 0], Q=0.001, R=0.1)

# Potential sensor inputs
x = 23.5
y = 40
theta = 0.32
ax = 4
ay = -0.4

# The measurement vector is what we observe, while the control vector is what we input.
# We provide some acceleration, and observe the position change
measurement = [[x], [y], [theta]]
controlVector = [[ax], [ay]]

# Add a measurement
kf.addMeasurement(measurement, controlVector)

# Pretty print the current state vector
kf.printValues()

# Print the raw numpy matrix current values
print(kf.X0)

```
> This input implies that our sensors are currently reading `x=1`, `y=2`, `θ=1.2`, `x"=1` and `y"=-1`
### How does it work?
The process is as follows:
```py
U = matrix(controlVector)
Xp = self.A * self.X0 + self.B * U
P = self.A * self.P0 * self.AT + self.Q
Y = matrix(measurement) - self.H * Xp
S = self.H * P * self.HT + self.R
K = P * self.HT * numpy.linalg.pinv(S)
self.X0 = Xp + K * Y
self.P0 = (self.I - K * self.H) * P
```

This may look confusing, but breaking it down should help.

##### A
`A` is the "state transition matrix" - a matrix that simply contains the physics formulas that is used in calculating `Xp`.

##### B
`B` is the "control matrix" . Like `A`, it takes our control inputs (in our case, the acceleration of the robot), and calculates how much this updates our current position.

##### U
`U` is the "control input vector". As the name implies, this is the input to the robot used to control it (i.e. inputs that would make our math prediction inaccurate). This is necessary because if the robot suddenly decelerates, this must be accounted for in the mathematical prediction. In our case, this is the acceleration of the robot [`x"`, `y"`] measured by the IMU.

##### Xp
`Xp` combines our **previous** state, `X0`, and our current inputs, `U`, and predicts where the robot will be **now**. However, this is only a *preliminary* prediction; it will be updated later by incorporating our position measurement.

##### P
P is the "state covariance matrix"- sort of the expected error in `Xp`. It describes the variances (and covariances) of each state variable. The higher the variance, the more uncertain the prediction of the variable in `Xp` is. `Q` is essentially the error associated with the mathematical equations of `Xp`, and will have to be experimented with during testing.

##### Y
Y is the "innovation" - this is just `measurement - prediction`. Notice the `H` matrix - this is the "observation matrix". This simply "selects" the values from the full state matrix that we are actually measuring.

##### S and K
These two are most easily explained together.
`K` is the Kalman gain - essentially a value from `0-1` saying "Do we trust the mathematical prediction or the measured values more?".

The Kalman gain is calculated as just: `Err(estimation) / (Err(estimation) + Err(measurement))`
`S` is the denominator, and `P * self.HT` is the numerator. 

`R` is `Err(measurement)` - this will be the expected errors in the sensors, some slight testing might be needed to narrow down the best value.

Again, the `H` matrix just "selects" the values that we are measuring- it does not modify the values in any way.

##### X0
We can now calculate our best estimate of the actual position. We simply take our mathematical prediction, `Xp` and add `K * Y` - the Kalman gain multiplied by `Y`.

Note that because `Y` is `measurement - Xp`, then `X0` will be:  
`K=0` => `Xp - 0` = `Xp`  
`K=1` => `Xp - (measurement - Xp)` = `measurement`

This demonstrates that the Kalman gain is simply a slider that decides how much weight to put in the prediction versus the measurement. 

Of course, `K` is a matrix, not a scalar, but this is the general idea.

##### P0
`P0` is essentially equal to: `(1-K) * P`, but `1` is replaced with `I`, the identity matrix, and K has to be multiplied by `H` to bring `K` up to the correct dimensions- it again does not change the values in any way. 

## TODO
- Gating - What if there is an extraneous measurement that says we our location is on Mars? This would obviously be incorrect and we could throw this measurement out. Without gating, this could cause the filter to diverge or behave strangely.
- Calculating Q and R - R can be found from the manufacturer information for the sensors (Remember, it's just the error in the measurement), but Q will have to be found by running tests with the robot
- Getting more inputs -The more measurements we make, the more accurate our position estimation will be. Can we calculate the velocity from our motor inputs? Would adding distance sensors help?
