from machine import Pin, I2C, PWM
from utime import sleep
from bmp280 import BMP280I2C
from machine import SoftI2C, Pin
from bno055 import *
from math import atan2, degrees
import _thread

# Initialize I2C buses and devices
i2c0 = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
bmp280 = BMP280I2C(0x77, i2c0)

i2c_imu = SoftI2C(sda=Pin(16), scl=Pin(17), timeout=1000)
imu = BNO055(i2c_imu)

# Initialize PWM for LED
LED_OUT = PWM(Pin(6))
LED_OUT.freq(1000)  # Set frequency to 1 kHz
LED_OUT.duty_u16(0)  # Initial brightness

# Shared variables for magnetometer data
shared_mag_x = 0
shared_mag_y = 0
data_lock = _thread.allocate_lock()
running = True  # Control flag for clean exit

def calculate_heading(mag_x, mag_y):
    """Calculate heading in degrees (0-360)."""
    heading = degrees(atan2(mag_y, mag_x))
    if heading < 0:
        heading += 360
    return heading

def core0_task():
    """Core 0 Task: Read sensor data and update shared magnetometer values."""
    global shared_mag_x, shared_mag_y, running
    calibrated = False

    while running:
        try:
            # Check calibration status
            if not calibrated:
                calibrated = imu.calibrated()
                print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))

            # Read BMP280 sensor data
            try:
                readout = bmp280.measurements
                print(f"Temperature: {readout['t']} °C, Pressure: {readout['p']} hPa.")
            except Exception as e:
                print(f"BMP280 error: {e}")

            # Read BNO055 magnetometer data
            try:
                mag_x, mag_y, mag_z = imu.mag()
                with data_lock:  # Safely update shared data
                    shared_mag_x, shared_mag_y = mag_x, mag_y
                    print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
                    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
                    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
            except Exception as e:
                print(f"BNO055 error: {e}")

        except Exception as e:
            print(f"Core 0 unexpected error: {e}")
        sleep(0.1)  # Sensor read interval

def core1_task():
    """Core 1 Task: Calculate heading and update LED PWM."""
    global shared_mag_x, shared_mag_y, running

    while running:
        try:
            # Access shared data
            with data_lock:
                mag_x, mag_y = shared_mag_x, shared_mag_y

            # Calculate heading
            heading = calculate_heading(mag_x, mag_y)
            print(f"Heading: {heading:.2f}°")

            # Adjust LED brightness based on heading
            angle_diff = abs(heading - 0)  # Difference from north
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            brightness = int((1 - angle_diff / 180) * 65535)

            # Update LED PWM with minimal delay
            LED_OUT.duty_u16(brightness)
            print(f"Brightness: {brightness}")

        except Exception as e:
            print(f"Core 1 unexpected error: {e}")

    print("Core 1 task terminated.")

# Start Core 1 for heading calculation and LED PWM
_thread.start_new_thread(core1_task, ())

# Run Core 0 task on the main core
try:
    core0_task()
except KeyboardInterrupt:
    print("Keyboard Interrupt. Cleaning up...")
    running = False
    sleep(0.5)  # Allow other threads to exit gracefully
    print("Program terminated.")
