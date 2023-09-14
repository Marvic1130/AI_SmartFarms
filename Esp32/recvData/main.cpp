#include Arduino.h
#include DHT.h


#define DHT_PIN 2           DHT22 데이터 핀
#define LIGHT_SENSOR_PIN 34  조도 센서 아날로그 핀
#define SOIL_SENSOR_PIN 35   토양 수분 센서 아날로그 핀

DHT dht(DHT_PIN, DHT22);

void setup() {
    Serial.begin(115200);
    dht.begin();
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int lightValue = analogRead(LIGHT_SENSOR_PIN);
    int soilValue = analogRead(SOIL_SENSOR_PIN);
    int co2Value = 0;   
    Serial.println(String(temperature) + , + String(humidity) + , + String(lightValue) + , + String(co2Value) + , + String(soilValue));
    delay(6000);
}


