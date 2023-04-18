# 2023 졸업프로젝트 - 인공지능기반 SmartParms

### 조원
| 학번        | 학과     | 파트            | 이름  |비고|
|-----------|--------|---------------|-----|---|
| 202010050 | 컴퓨터공학과 | 머신러닝, 디바이스 개발 | 강예성 |**팀장**|
| 201910057 | 컴퓨터공학과 | 디바이스 개발       | 유제원 |**부팀장**|
| 201910048 | 컴퓨터공학과 | 프론트엔드         | 강민성 |
| 202010056 | 컴퓨터공학과 | 디바이스 개발       | 문예진 |
| 201910058 | 컴퓨터공학과 | 머신러닝          | 이동휘 |


## 개요

### What's Smart Parms?

스마트 팜은 **정보기술을 이용하여** 농작물 재배 시설의 온도 · 습도 · 햇볕량 · 이산화탄소 · 토양 등을 측정 분석하고, 분석 결과에 따라서 제어 장치를 구동하여 적절한 상태로 변화시킨다.
그리고 스마트폰과 같은 모바일 기기를 통해 원격 관리도 가능하다. 
스마트 팜으로 농업의 생산 · 유통 · 소비 과정에 걸쳐 생산성과 효율성 및 품질 향상 등과 같은 고부가가치를 창출시킬 수 있다.

_**[<나무위키>](https://namu.wiki/w/스마트%20팜)**_

***

### 주제 선정 이유 및 기대효과
Smart Parms은 IOT, Machine Learning 기술이 발달하면서 각광받고있는 분야로,
농업생산량을 크게 증가시킬 수 있는 사업모델이다.

이 프로젝트의 차별성은 AWS를 사용하여 소규모 농장부터 대규모 농장까지 시설의 환경 데이터, 제어 데이터를 쉽게 관리할 수 있고,
Matter통신을 이용하여 특정 앱이 아닌 여러 IT기업에서 만든 IOT앱에서 농장을 쉽게 관리할 수 있도록 한다.

***

### 개발 방법및 구현 기술

1. RaspberryPi를 이용하여 스마트 미러의 외관을 가지는 IoT Hub를 개발
2. ESP32를 이용하여 각 농장, 밭, 논의 상태를 모니터링 및 제어
3. 모듈에서 RaspberryPi로 데이터를 보낼 때 WiFi통신을 이용하여 데이터 및 제어 명령 송수신
4. Hub로 전송된 데이터는 AWS를 사용하여 데이터베이스에 저장
5. 저장된 데이터를 학습 후 인공지능이 Farms의 상태를 진단하며 자동관리
6. Matter통신을 이용하여 Apple Homekit, Samsung SmartThings 등 여러 IOT앱으로 스마트팜을 제어

***

## 기술 스텍 및 프로젝트 구성도

### 제어, Sensing모듈

* Arduino, Esp32같은 MCU를 사용
* WiFi 통신
* Actuator - Servo motor, DC motor, Stepping motor, LCD 등
* Sensor - 온습도, 토양질 센서, 수위감지 센서, 조도센서 등

### HUB

* RaspberryPi
* WiFi 통신
* Matter 통신
* Socket 통신

### Web Service & DataBase

* Spring Framework
* React
* MySQL
* AWS RDS

### Machin Learning

* Tensorflow
* Multiple Linear Regression
* RNN(Recurrent neural network)
* 양방향 LSTM
* Socket 통신

