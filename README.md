# ESP32 WiFi Tarama ve Trilaterasyon (RSSI ile Konum Tahmini)

Bu proje, ESP32 ile çevredeki WiFi ağlarını tarayıp SSID ve RSSI değerlerini seri port üzerinden bilgisayara gönderir.  
Bilgisayar tarafında çalışan bir Python script'i, bu RSSI değerlerini kullanarak yaklaşık mesafe hesaplar ve daha önce konumu bilinen erişim noktalarına göre basit bir *trilaterasyon* tahmini yapar.

## Donanım

- ESP32 DevKit (esp32dev)
- USB kablo

Ek bağlantıya gerek yok; sadece USB ile bilgisayara bağlı olması yeterli.

## Kullanılan Teknolojiler

- ESP32 + Arduino framework (PlatformIO ile)
- Python 3
- pyserial, scipy, math, datetime

---

## ESP32 Kodu (WiFi Tarama)

ESP32 tarafında kullanılan örnek kod:

```cpp
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