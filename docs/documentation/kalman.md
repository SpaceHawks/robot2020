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

Output:
> x: 23.571394574012373
y: 39.9428843407901
θ: 0.3047691575440266
x': 3.2860542598762494
y': 0.1711565920990018
w: 0.15230842455973345

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
self.runAdaptiveFilter(Y, S)
```

This may look confusing, but breaking it down should help.

##### U
`U` is the "control input vector". As the name implies, this is the input to the robot used to control it (i.e. inputs that would make our math prediction inaccurate). This is necessary because if the robot suddenly decelerates, this must be accounted for in the mathematical prediction. In our case, this is the acceleration of the robot [`x"`, `y"`] measured by the IMU.

##### A
`A` is the "state transition matrix" - a matrix that simply contains the physics formulas that is used in calculating `Xp`.

##### B
`B` is the "control matrix" . Like `A`, it takes our control inputs (in our case, the acceleration of the robot), and calculates how much this updates our current position.

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

##### Adaptive Filter
The `runAdaptiveFilter` method simply takes in the Y (residual) and S (error in the residual) and computes:  
`E = Y² / S`

On *average*, we expect the value of E to be zero (Remember, `Y` is the difference between what we expected and what we measured; due to Gaussian probabilities, this should be zero). However, when the measurement differs greatly from `Xp` (the mathematical prediction), `E` will have a rather large value. `S` sort of normalizes `Y²` to account for measurement errors. 

We can assume that by setting a threshold for `E`, we can determine when the robot is making a manuever (speeding up, turning, etc.). This value should be high enough that random noise won't be detected as a manuever. When this occurs, the value for `Q`, the error in our mathematical prediction, should be increased. This means that during the time the manuever is taking place, more weight will be placed with the measurements. 

As soon as the mathematical model and measurements converge again, the value of `Q` is lowered back to its starting value.

Example of no adpative filter vs. adaptive filter:
![Eventually converges, but not immediately](https://i.imgur.com/2QiUl6k.png)
![Converges much more quickly](https://i.imgur.com/CAeJ9of.png)

<details><summary>Code for generating graphs</summary>
<p>

```python
from kalman import KalmanFilter
import numpy
import matplotlib.pyplot as plt
import random

# Note the 0. is important - it needs to be a float matrix
kf = KalmanFilter(dt=0.5, stateMatrix=[0., 0, 0, 0, 0, 0], Q=0.00000001, R=0.1, std=100, adaptive=True)

trueVals = [[], []]
sensorVals = [[], []]
kfVals = [[], []]
for i in numpy.linspace(0, 200, 400):
    n = 0
    if i >= 57:  # Change in direction
        n = 2 * (i - 57)

    x = i + n + random.gauss(0, 1)  # Measurement noise
    y = 2 * i + random.gauss(0, 1)  # Measurement noise

    ax = 0
    ay = 0
    kf.addMeasurement([[x], [y], [0]], [[ax], [ay]])

    trueVals[0].append(i + n)
    trueVals[1].append(2 * i)
    sensorVals[0].append(x)
    sensorVals[1].append(y)
    kfVals[0].append(kf.X0.tolist()[0][0])
    kfVals[1].append(kf.X0.tolist()[1][0])

# Pretty print the current state vector
kf.printValues()

plt.scatter(trueVals[0], trueVals[1], label='True values', color='r')
# plt.scatter(sensorVals[0], sensorVals[1], label='Sensor values', color='g')
plt.scatter(kfVals[0], kfVals[1], label='KF values', color='b')
plt.xlabel('x')
plt.ylabel('y')
plt.title(("With" if kf.adaptive else "Without") + ' adaptive filtering')
plt.legend()
plt.show()

```

</p>
</details>

## TODO
- Gating - What if there is an extraneous measurement that says we our location is on Mars? This would obviously be incorrect and we could throw this measurement out. Without gating, this could cause the filter to diverge or behave strangely, especially with the adaptive filter. Testing will determine if this is necessary or not.
- Calculating Q and R - R can be found from the manufacturer information for the sensors (Remember, it's just the error in the measurement), but Q will have to be found by running tests with the robot
- Getting more inputs -The more measurements we make, the more accurate our position estimation will be. Can we calculate the velocity from our motor inputs? Would adding distance sensors help?
