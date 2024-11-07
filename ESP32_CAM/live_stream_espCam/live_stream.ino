#include "esp_camera.h"
#include <WiFi.h>

const char* ssid = "GatorCam";
const char* password = "Gator1234";

WiFiServer server(80);

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

void setup() {
  Serial.begin(115200);
  Serial.println();

  WiFi.softAP(ssid, password);
  Serial.println("WiFi AP started");

  // Camera configuration
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;  // Set to 480p resolution
  config.jpeg_quality = 10;           // Adjust quality for better performance
  config.fb_count = 1;                // Use 1 buffer for now

  if (psramFound()) {
    config.fb_count = 2;  // Use 2 buffers if PSRAM is available
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  server.begin();
  Serial.println("HTTP server started");

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.softAPIP());
  Serial.println("' to connect");
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    String req = client.readStringUntil('\r');
    client.flush();

    if (req.indexOf("GET /") != -1) {
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
      client.println();

      while (client.connected()) {
        camera_fb_t *fb = esp_camera_fb_get();
        if (!fb) {
          Serial.println("Camera capture failed");
          client.stop();
          return;
        }

        client.print("--frame\r\n");
        client.print("Content-Type: image/jpeg\r\n");
        client.print("Content-Length: ");
        client.print(fb->len);
        client.print("\r\n\r\n");
        client.write(fb->buf, fb->len);
        client.print("\r\n");

        esp_camera_fb_return(fb);

        delay(33);  // Control the frame rate to ~30 FPS
      }
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}
