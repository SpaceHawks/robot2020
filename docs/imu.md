# IMU

### Purpose
Simply reads gyroscope and accelerometer data from the IMU (`SEN-11028 MPU 6050`)

### Example Usage
```py
from imu import IMU
imu = IMU()
accs = imu.readAccelerometer()
# accs will be [ax, ay, az]
```
