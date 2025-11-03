#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  Serial.println("WiFi scanning...");
}

void loop() {
  int n = WiFi.scanNetworks();
  Serial.println("scan done");

  if (n == 0) {
    Serial.println("no networks found");
  } else {
    for (int i = 0; i < n; ++i) {
      Serial.print("SSID: ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" RSSI: ");
      Serial.println(WiFi.RSSI(i));
      delay(10);
    }
  }
  delay(5000);
}