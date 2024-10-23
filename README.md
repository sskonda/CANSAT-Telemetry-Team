Telemetry Subsystem for SSDC CANSAT Competition
Overview
This repository contains the telemetry subsystem code and resources for the SSDC CANSAT competition. It focuses on the integration and operation of sensors, motors, and the power subsystem, which are essential components for gathering, processing, and transmitting flight data. The repository does not include the flight software but provides all necessary libraries, configuration files, and guidelines for testing and deploying individual components.

Project Background
The CANSAT competition involves designing a small satellite (payload) and container that are deployed from a rocket. Upon reaching peak altitude, the container descends using a parachute, while the payload separates mid-flight and uses an auto-gyro system for controlled descent. During the entire mission, the payload must transmit telemetry data to the ground station at 1 Hz.

The telemetry subsystem covered in this repository includes the following key responsibilities:

Collecting sensor data: temperature, battery voltage, altitude, gyro rotation rate, acceleration, magnetic field, and GPS coordinates.
Managing power subsystems to ensure consistent operation throughout the flight.
Handling data transmission to the ground station.
Repository Structure
Libraries: Contains the necessary sensor and motor libraries, which need to be uploaded to the microcontroller (e.g., Raspberry Pi Pico) for compatibility with the Thonny IDE.
Power Subsystem: Configuration files and scripts to manage power distribution and battery status monitoring.
Sensor Integration: Example code and test files for sensors, such as temperature, GPS, gyroscopes, and magnetometers, ensuring accurate data collection.
Motor Control: Scripts to manage motors or actuators involved in the payload’s auto-gyro descent mechanism.
Setup Instructions
Installing Libraries:

For libraries to work in the Thonny IDE, you must place the include files (i.e., libraries) directly into the storage of the microcontroller (such as the Raspberry Pi Pico).
Main scripts for testing can remain on the computer or development environment.
Testing the Subsystem:
Use individual test scripts provided in the repository to validate each sensor and motor module. Ensure that data is properly transmitted to the ground station at the required 1 Hz interval during testing.

Contribution Guidelines
Branching: Use feature-specific branches to add or modify subsystem components.
Documentation: Update the README or relevant code comments with clear descriptions of any changes.
Testing: All code must be tested on the target hardware before merging into the main branch.
Future Work
Integrate all subsystem components with the flight software.
Conduct full end-to-end testing of telemetry data transmission to the ground station.
Implement fault-tolerant mechanisms for power and communication systems during flight.
