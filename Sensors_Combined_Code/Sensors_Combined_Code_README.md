# Sensors Combined Code

## First Iteration
- Combine the BNO055 sensor code and the BMP280 sensor code so that both sensors readings are being displayed at the same time

## Second Iteration
- Add GPS code to the existing code with the BMP280 and the BNO055 sensor so that all telemetry data is being displayed at the same time

## Third Iteration
- Integrate XBEE radio transmitter and receiver to the code so that the telemetry system data collected from the BNO055, BMP280, and the Adafruit Ultimate GPS is transmitted to another XBEE radio that is connected to the ground station, to ensure packets are recieved with minimal loss

## Fourth Iteration
- Add Magnetometer code so that the servo motor controls the ESP32 CAM direction and makes it face in the direction of magnetic North at all times

## Fifth Iteration
- Add code to toggle a GPIO port to turn on both cameras in the onboard telemetry system with a command from the ground stationn GUI



