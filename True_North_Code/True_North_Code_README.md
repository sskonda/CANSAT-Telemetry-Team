# This is the folder for using the BNO055 sensor's magentometer to find magnetic north

## LED Compass
- Write code to find magnetic north
- Control the brightness of an LED using PWM signals from the PI pico

---

### LED Compass with Memory Management
- **Purpose:** to see where the program is crashing and to fix any potential I2C bus contentions and any repeated use of objects without proper cleanup

---

### LED Compass with Threading
- Implement multicore processing with the LED compass code
  - Core 0: Reads and displays sensor data
  - Core 1: Calculates and adjusts LED brightness via a PWM signal that responds to the calculated heading of the magnetometer
- **Problems:** errors occure when exiting the program, there seems to be more than ideal latency on the LED PWM signal

---


### Reduced Latency LED Compass with Threading code
#### Why Multi-Core Processing is Useful
Multi-core processing allows tasks to run in parallel, enabling efficient resource utilization and faster response times. In this project:
- **Core 0** is dedicated to reading sensor data from the BMP280 (temperature and pressure) and BNO055 (magnetometer).
- **Core 1** calculates the heading from the magnetometer data and updates the LED brightness through a PWM signal.

This separation ensures that computationally intensive tasks, such as heading calculation and PWM signal updates, do not block or delay the sensor reading process.


#### How Multi-Core Processing is Implemented
The project uses Python's `_thread` library to create lightweight threads:
1. **Core 0** runs the `core0_task` function:
   - Reads sensor data from the BMP280 and BNO055.
   - Updates shared magnetometer data (`mag_x`, `mag_y`) using a thread-safe **lock** to avoid race conditions.
2. **Core 1** runs the `core1_task` function:
   - Calculates the heading based on the magnetometer data.
   - Adjusts the LED's brightness using a PWM signal.


#### Safeguards Against Contentions
To ensure smooth and error-free operation in a multi-threaded environment:
1. **Shared Data Protection**:
   - Magnetometer data (`mag_x` and `mag_y`) is shared between the two threads.
   - A `data_lock` is used to ensure only one thread accesses or updates the shared data at a time.
   - This prevents race conditions and data corruption during simultaneous read/write operations.
2. **Minimal Lock Usage**:
   - Locks are held only for the brief period needed to copy the shared data, minimizing the impact on performance.


#### The `running` Variable
The `running` variable acts as a global control flag for both threads:
- **Purpose**:
  - When set to `True`, both threads execute their respective tasks.
  - When set to `False`, the threads terminate gracefully.
- **Keyboard Interrupt**:
  - Press `Ctrl+C` to trigger a `KeyboardInterrupt` in the main thread.
  - This sets `running = False`, signaling both threads to stop execution.
  - A brief delay (`sleep(0.5)`) ensures both threads exit cleanly before the program terminates.


## Servo Compass
- Modify the first iteration code to work with a 360 degree servo motor
  - The Servo motor should point north at all times, taking input from th gyroscope to know which way it should adjust

## Camera Compass
- Modify the code so that it points the camera to the direction of magnetic north and keeps it there, adjusting for any movement by taking readings from the Gyroscope
