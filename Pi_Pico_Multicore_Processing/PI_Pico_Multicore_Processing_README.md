# This is the Folder for Using Multicore Processing on a Raspberry Pi Pico

## Overview
This folder contains code and resources for implementing multicore processing on a Raspberry Pi Pico. The goal is to explore how multicore processing works and to optimize telemetry tasks for lower latency and higher efficiency.

## Test Folder
The `test` folder in this directory is intended for experimenting with multicore processing. Basic examples will demonstrate how to utilize both cores of the Raspberry Pi Pico. These examples will serve as a foundation for splitting telemetry tasks across cores effectively.

## Task Allocation for Multicore Processing
To ensure efficient parallelism and reduced latency, we propose the following allocation of tasks:

### Core 0 (Primary Core)
- **Sensor Data Acquisition**: Handles communication with sensors (e.g., BMP280, magnetometer) via I2C or SPI.
- **Data Processing**: Computes derived values such as altitude, heading, or tilt from raw sensor data.

### Core 1 (Secondary Core)
- **Data Transmission**: Formats and transmits telemetry data via communication interfaces (e.g., UART, LoRa, or Wi-Fi).
- **Data Logging**: Saves data to an SD card or other storage to ensure no loss of critical telemetry information.

## Getting Started
1. Clone the repository and navigate to the `Pi_Pico_Multicore_Processing` folder.
2. Explore the `test` folder to familiarize yourself with basic multicore processing examples.
3. Modify the provided code to integrate your sensor data acquisition and telemetry transmission tasks.

## References
- [Raspberry Pi Pico Python SDK Documentation](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)
- [Raspberry Pi Pico SDK GitHub Repository](https://github.com/raspberrypi/pico-sdk)
- [Rasberry Pi Pico Getting Started](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
