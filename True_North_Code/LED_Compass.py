#This code seems to crash frequently we need to find a way to fix this so that this doesn't become an issue during launch

from machine import Pin, I2C, PWM
from utime import sleep
from bmp280 import BMP280I2C
from machine import SoftI2C, Pin
from bno055 import *
from math import atan2, degrees

i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
bmp280_i2c = BMP280I2C(0x77, i2c0)  # address may be different

i2c_imu = SoftI2C(sda=Pin(16), scl=Pin(17), timeout=1000)
imu = BNO055(i2c_imu)

# just checking
print("Connected I2C devices:", i2c0.scan())

# PWM pin 6
LED_OUT = PWM(Pin(6))
LED_OUT.freq(1000)
# Set duty cycle to 50%
LED_OUT_brightness = int(65536*0.5)
LED_OUT.duty_u16( LED_OUT_brightness ) #out of 65536)

def calculate_heading(mag_x, mag_y):
    # Calculate heading in degrees (0-360)
    heading = degrees(atan2(mag_y, mag_x))  # atan2 handles correct quadrant for (x, y)
    if heading < 0:
        heading += 360
    return heading

calibrated = False
while True:
    #sleep(1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    
    #BMP280
    readout = bmp280_i2c.measurements
    print(f"Temperature: {readout['t']} °C, pressure: {readout['p']} hPa.")
    
    #BNO055
    print('Temperature {}°C'.format(imu.temperature()))
    print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
    
    # Read magnetometer data
    mag_x, mag_y, mag_z = imu.mag()
    heading = calculate_heading(mag_x, mag_y)
    print(f"Heading: {heading:.2f}°")

    # Determine brightness based on proximity to magnetic north (0°)
    angle_diff = abs(heading - 0)  # Difference from magnetic north
    if angle_diff > 180:  # Adjust to smallest angular difference
        angle_diff = 360 - angle_diff
    
    brightness = int((1 - angle_diff / 180) * 65535)  # Full brightness at 0°, dimmest at 180°
    LED_OUT.duty_u16(brightness)
    print(f"Brightness: {brightness}")

    sleep(0.1)