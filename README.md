
# Telemetry Subsystem for SSDC CANSAT Competition  

## Overview  
This repository contains the telemetry subsystem code and resources for the SSDC CANSAT competition. It focuses on the integration and operation of sensors, motors, and the power subsystem, which are essential components for gathering, processing, and transmitting flight data. The repository does **not** include the flight software but provides all necessary libraries, configuration files, and guidelines for testing and deploying individual components.

## Project Background  
The CANSAT competition involves designing a small satellite (payload) and container that are deployed from a rocket. Upon reaching peak altitude, the container descends using a parachute, while the payload separates mid-flight and uses an auto-gyro system for controlled descent. During the mission, the payload must transmit telemetry data to the ground station at 1 Hz. 

The telemetry subsystem covered in this repository includes the following key responsibilities:
- **Collecting sensor data**: temperature, battery voltage, altitude, gyro rotation rate, acceleration, magnetic field, and GPS coordinates.
- **Managing power subsystems** to ensure consistent operation throughout the flight.
- **Handling data transmission** to the ground station.

## Repository Structure  
- **Individual Sensors Names**: Contains the necessary sensor and motor libraries, which must be uploaded to the microcontroller (e.g., Raspberry Pi Pico) for compatibility with the Thonny IDE.
- **CANSAT_PCB_Files**: Configuration files and scripts to manage power distribution and battery status monitoring.
- **`Sensor Integration/`**: Example code and test files for sensors such as temperature, GPS, gyroscopes, and magnetometers, ensuring accurate data collection.
- **`Motor Control/`**: Scripts to manage motors or actuators involved in the payload’s auto-gyro descent mechanism.

## Setup Instructions  
1. **Installing Libraries**:  
   - Place the include files (libraries) directly into the storage of the microcontroller (such as the Raspberry Pi Pico) to use them in Thonny.  
   - Main scripts for testing can remain in the development environment on your computer.

2. **Testing the Subsystem**:  
   Use individual test scripts provided in the repository to validate each sensor and motor module. Ensure that the telemetry data is transmitted to the ground station at the required **1 Hz interval** during testing.

## Software Raspberry Pi PIco connections for CANSAT (i.e. whcih GPIO Pins are connected to What)

 - **GP 6** PWM for LED to point Bottom Camera North
 - **GP 7 PWM** for Servo to point Bottom Camera North

 - **GP 8** BMP280 SDA
 - **GP 9** BMP280 SCL

 - **GP 12** Adafruit Ultimate GPS TX (UART Transmit)
 - **GP 13** Adafruit Ultimate GPS RX (UART Receive)

 - **GP 16** BNO055 SDA
 - **GP 17** BNO055 SCL

## Contribution Guidelines  
1. **Branching**: Use feature-specific branches to add or modify subsystem components.  
2. **Documentation**: Update the README or relevant code comments with clear descriptions of any changes.  
3. **Testing**: All code must be tested on the target hardware before merging into the main branch.

## Future Work  
- Integrate all subsystem components with the flight software.  
- Conduct full end-to-end testing of telemetry data transmission to the ground station.  
- Implement fault-tolerant mechanisms for power and communication systems during flight.
- Finish Coding INA260 Sensor and adding state machine logic for the controlling of other actuators on the CANSAT
- Program and Test XBEE radios (make sure they are actually transmitting to the GUI)

