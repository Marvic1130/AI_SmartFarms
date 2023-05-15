#include <WiFi.h>
#include "DHT.h"
#include "ESP32Servo.h"

const char* ssid = "Lab403_2.4G"; // WiFi SSID
const char* password = "00000000"; // WiFi Password
const char* host = "192.168.1.3"; // 라즈베리 파이 서버의 IP 주소
const int port = 8888; // 라즈베리 파이 서버에서 사용하는 포트 번호
const int dht_pin = 16; // DHT22가 연결된 핀 번호
const int led_pin[3] = {17, 18, 19}; // LED가 연결된 핀 번호
const int fan_pin = 25;

Servo servo;
WiFiClient client;
DHT dht(dht_pin, DHT22);

String splitString(String &msg, String delimiter){
  int index = 0;
  index = msg.indexOf(delimiter);
  String token = msg.substring(0, index);
  msg = msg.substring(index + 1);

  return token;
}

void setup() {
  Serial.begin(115200);
  for(int i = 0; i < 3; i++)
    pinMode(led_pin[i], OUTPUT);
  pinMode(fan_pin, OUTPUT);
  servo.attach(4);
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

    String response = client.readStringUntil('\n');
    Serial.println("Response from server: " + response);
    String delimiter = ", ";
    setLedState(led_pin, splitString(response, delimiter));
    setFanState(fan_pin, splitString(response, delimiter));
    setServoState(servo, splitString(response, delimiter));

    client.stop(); // 연결 종료

  } else {
    Serial.println("Connection failed");
  }

  delay(100);
}
