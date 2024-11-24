#include <Adafruit_GPS.h>

#define GPS_TX_PIN 7 
#define GPS_RX_PIN 8

String GPS_TIME = "00:00:00";

SoftwareSerial GPS_USART(8, 7);   //USART for GPS

Adafruit_GPS GPS(&GPS_USART);
uint32_t timer = millis();vv

void setup() {
  Serial.begin(115200);
  GPS.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
}

void loop() {
  char c = GPS.read();

    if (GPS.newNMEAreceived()) {

      if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
        return;  // we can fail to parse a sentence in which case we should just wait for another
    }

  if (millis() - timer > 2000) {
    timer = millis(); // reset the timer

    Serial.print("Hour: ");
    Serial.println(GPS.hour);

    Serial.print("Minutes: ");
    Serial.println(GPS.minute);

    Serial.print("seconds: ");
    Serial.println(GPS.seconds);

    Serial.print("Latitude: ");
    Serial.println(GPS.latitude);

    Serial.print("Longitude: ");
    Serial.println(GPS.longitude);

    Serial.print("Altitude: ");
    Serial.print(GPS.altitude);

    Serial.print("Sats: ");
    Serial.print(GPS.satellites);

  }


}