from machine import Pin, I2C, PWM, SoftI2C
from utime import sleep
from bmp280 import BMP280I2C
from bno055 import *
from math import atan2, degrees
import _thread

# Initialize I2C buses and devices
i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
bmp280_i2c = BMP280I2C(0x77, i2c0)

i2c_imu = SoftI2C(sda=Pin(16), scl=Pin(17), timeout=1000)
imu = BNO055(i2c_imu)

# Initialize PWM for LED
LED_OUT = PWM(Pin(6))
LED_OUT.freq(1000)
LED_OUT.duty_u16(int(65536 * 0.5))  # Set initial brightness to 50%

# Global variables for communication between threads
shared_mag_x = 0
shared_mag_y = 0
data_lock = _thread.allocate_lock()  # Mutex to protect shared data

def calculate_heading(mag_x, mag_y):
    """Calculate heading in degrees (0-360)."""
    heading = degrees(atan2(mag_y, mag_x))
    if heading < 0:
        heading += 360
    return heading

def core0_task():
    """Core 0: Read and display sensor data."""
    global shared_mag_x, shared_mag_y

    calibrated = False
    while True:
        try:
            # Check calibration status
            if not calibrated:
                calibrated = imu.calibrated()
                print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))

            # Read BMP280 sensor data
            try:
                readout = bmp280_i2c.measurements
                print(f"Temperature: {readout['t']} °C, Pressure: {readout['p']} hPa.")
            except Exception as e:
                print(f"BMP280 error: {e}")

            # Read BNO055 sensor data
            try:
                with data_lock:  # Lock to update shared data
                    mag_x, mag_y, mag_z = imu.mag()
                    shared_mag_x, shared_mag_y = mag_x, mag_y
                print(f"Magnetometer Data: x={mag_x}, y={mag_y}, z={mag_z}")
            except Exception as e:
                print(f"BNO055 error: {e}")

            sleep(0.1)  # Adjust delay as needed
        except KeyboardInterrupt:
            print("Core 0 task stopped.")
            break
        except Exception as e:
            print(f"Core 0 unexpected error: {e}")

def core1_task():
    """Core 1: Calculate heading and adjust LED brightness."""
    global shared_mag_x, shared_mag_y

    while True:
        try:
            with data_lock:  # Lock to safely read shared data
                mag_x, mag_y = shared_mag_x, shared_mag_y

            # Calculate heading
            heading = calculate_heading(mag_x, mag_y)
            print(f"Heading: {heading:.2f}°")

            # Adjust LED brightness based on heading
            angle_diff = abs(heading - 0)  # Difference from magnetic north
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            brightness = int((1 - angle_diff / 180) * 65535)
            LED_OUT.duty_u16(brightness)
            print(f"Brightness: {brightness}")

            sleep(0.1)  # Adjust delay as needed
        except KeyboardInterrupt:
            print("Core 1 task stopped.")
            break
        except Exception as e:
            print(f"Core 1 unexpected error: {e}")

# Start Core 1
_thread.start_new_thread(core1_task, ())

# Run Core 0 task on main core
core0_task()
