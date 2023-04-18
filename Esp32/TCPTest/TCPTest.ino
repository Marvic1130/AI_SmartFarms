#include <WiFi.h>
#include "DHT.h"

const char* ssid = "Lab403_2.4G";         // WiFi SSID
const char* password = "00000000"; // WiFi Password
const char* host = "192.168.1.3";     // 라즈베리 파이 서버의 IP 주소
const int port = 8888;                 // 라즈베리 파이 서버에서 사용하는 포트 번호
const int dht_pin = 16;                 // DHT22가 연결된 핀 번호
const int led_pin = 17;                 // LED가 연결된 핀 번호

WiFiClient client;
DHT dht(dht_pin, DHT22);

void setup() {
  Serial.begin(115200);
  pinMode(led_pin, OUTPUT);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected");
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(1000);
    return;
  }
  
  String message = "Temperature: " + String(temperature) + "C, Humidity: " + String(humidity) + "%";
  Serial.println(message);

  if (client.connect(host, port)) {
    Serial.println("Connected to server");
    client.println(message);  // 서버로 메시지 전송
    while (client.connected()) {
      // 라즈베리 파이가 보낸 응답을 받아옵니다.
      if (client.available()) {
        String response = client.readStringUntil('\n');
        Serial.println("Response from server: " + response);
        if (response.indexOf("True") >= 0) {  // 메시지에 "error"가 포함되어 있다면 LED를 켭니다.
          digitalWrite(led_pin, HIGH);
          break;
        } else if(response.indexOf("False") >= 0){
          digitalWrite(led_pin, LOW);
          break;
        }
        break;
      }
    }
    client.stop(); // 연결 종료
  } else {
    Serial.println("Connection failed");
  }

  delay(50);
}
