"""
Simple implementation of Kalman Filter using IMU and LIDAR
"""
# TODO Gating (maybe), calculating Q and R, etc.

import numpy
matrix = numpy.matrix  # I just want my life to be easier


class KalmanFilter:
    def __init__(self, dt=1, stateMatrix=[0, 0, 0, 0, 0, 0], Q=0.0001, R=0.02, std=6):
        # Measurement time interval
        self.dt = dt

        # Initial values - these values don't have to be exact, just estimated
        self.X0 = matrix(stateMatrix).T  # State matrix

        # State transition matrix
        self.A = matrix(
            [
                [1, 0, 0, dt, 0, 0],
                [0, 1, 0, 0, dt, 0],
                [0, 0, 1, 0, 0, dt],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1],
            ])

        # Control update matrix
        self.B = matrix(
            [
                [0.5 * dt ** 2, 0],
                [0, 0.5 * dt ** 2],
                [0, 0],
                [dt, 0],
                [0, dt],
                [0, 0]
            ]
        )

        # State transitional transpose
        self.AT = self.A.T

        # Error covariance matrix
        self.P0 = numpy.eye(self.A.shape[0])

        # Observation matrix - We are only observing (measuring) x, y, and theta
        self.H = matrix([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
        ])

        # Transformation transpose
        self.HT = self.H.T

        # Identity matrix
        self.I = matrix(numpy.eye(self.A.shape[0]))

        # Measurement noise covariance
        self.R = matrix(numpy.eye(self.H.shape[0])) * R

        # Process error covariance
        self.Q = matrix(numpy.diag([0, 0, 0, Q, Q, Q]))

        # ADAPTIVE FILTER VARIABLES

        # Number of standard deviations for adaptive filter to kick in
        self.std = std

        # Count for times Q has been incremented for the adaptive filter
        self.count = 0

        # How much to scale Q by for adaptive filter
        self.Q_scale = 1000

    def addMeasurement(self, measurement, accVector):
        U = matrix(accVector)  # Control input vector
        Xp = self.A * self.X0 + self.B * U
        P = self.A * self.P0 * self.AT + self.Q
        Y = matrix(measurement) - self.H * Xp
        S = self.H * P * self.HT + self.R
        K = P * self.HT * numpy.linalg.pinv(S)
        self.X0 = Xp + K * Y
        self.P0 = (self.I - K * self.H) * P

        # Update Q if measurement was way off (or if the measurement has returned to more likely values)
        # This should activate when the robot manuevers so that the model can correct itself quickly
        self.runAdaptiveFilter(Y, S)
        return self.X0

    def runAdaptiveFilter(self, Y, S):
        E = Y.T * S.I * Y
        if E > self.std:
            self.Q *= self.Q_scale
            self.count += 1
        elif self.count > 0:
            self.Q /= self.Q_scale
            self.count -= 1

    def printValues(self):
        vals = self.X0.tolist()
        p1 = "x: " + str(vals[0][0]) + "\ny: " + str(vals[1][0]) + "\nθ: " + str(vals[2][0])
        p2 = "x': " + str(vals[3][0]) + "\ny': " + str(vals[4][0]) + "\nw: " + str(vals[5][0])
        print(p1 + '\n' + p2)
