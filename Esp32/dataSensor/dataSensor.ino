#include <Arduino.h>
#include <DHT.h>
#include <cm1106_i2c.h>

#define DHT_PIN 2            // DHT22 데이터 핀
#define LIGHT_SENSOR_PIN 34  // 조도 센서 아날로그 핀
#define SOIL_SENSOR_PIN 35   // 토양 수분 센서 아날로그 핀

DHT dht(DHT_PIN, DHT22);
CM1106_I2C cm1106_i2c;

int co2Value = 0;
float temperature = 0;
float humidity = 0;
int lightValue = 0;
int soilValue = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();
  cm1106_i2c.begin();
  cm1106_i2c.read_serial_number();
  delay(1000);
}

void loop() {
  uint8_t ret = cm1106_i2c.measure_result();
  if (ret == 0) {
    co2Value = cm1106_i2c.co2;
  }
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  lightValue = analogRead(LIGHT_SENSOR_PIN);
  soilValue = analogRead(SOIL_SENSOR_PIN);

  Serial.println(String("1") + "," + String(temperature) + "," + String(humidity) + "," + String(lightValue) + "," + String(co2Value) + "," + String(soilValue));
  delay(6000);
}
