import RPi.GPIO as GPIO
import socket
import json
import requests
from time import sleep

# 서버 정보
HOST = '0.0.0.0'  # 서버의 IP 주소.
PORT = 8081  # 서버에서 사용할 포트 번호.

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

server_url = 'https://smartfarmhansei.shop/sensor/data'  # 웹 서버의 URL

# 초기화

generation_mode = 0

led_pin_1 = 13
#led_pin_2 = 
water_pump_pin_1 = 19
#water_pump_pin_2 = 

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_pin_1, GPIO.OUT)
GPIO.setup(water_pump_pin_1, GPIO.OUT)

GPIO.output(led_pin_1, GPIO.LOW)
GPIO.output(water_pump_pin_1, GPIO.LOW)

# status & value
# 현재 센서값은 임의의 값 출력을 위해서 값을 일단 넣은 상태
# 이후 socket 통신으로 센서값을 받는 코드를 작성하고 값을 변수에 받을 예정
# 0 = Non
light_val = 0
temp_val = 0
humi_val = 0
Co2_Val = 0
Soil_Val = 0

# actuator의 기본값 설정 이후 제어를 통해서 값을 변경하고 그 값에 따라 actuator 제어
fan_status = False
window_status = False


led_status_1 = False
led_status_2 = False
led_status_3 = False
led_status_4 = False

pump_status_1 = False
pump_status_2 = False
pump_status_3 = False
pump_status_4 = False

class SensorModule:
    def __init__(self, Id, light_val, temp_val, humi_val, Co2_val, Soil_val):
        self.id = Id
        self.lightVal = light_val
        self.tempVal = temp_val
        self.humiVal = humi_val
        self.Co2Val = Co2_val
        self.SoilVal = Soil_val


def send_to_server(url, data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)


# Loop

# 0 : Auto Mode
# 1 : manual
generation_mode = input("hello hansei Farm ^-^ start setting mode : ")

while True:
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    if generation_mode == 1:
        print("Manual Mode 0N")
        while True:
            control = input("input number 0 ~ 2 : ")   # 0 recv data, 1 led, 2 pump
            if control == 0 :
                data = client_socket.recv(1024)  # 클라이언트로부터 데이터를 받는다.
                if not data:
                    print("None Data")
                    break
                
                data_str = data.decode()
                sensor_id,temp_val, humi_val, light_val, Co2_Val, Soil_Val = map(float, data_str.split(','))
                
                # 센서 데이터 객체 생성
                sensor_data = SensorModule(sensor_id, light_val, temp_val, humi_val, Co2_Val, Soil_Val)
                filename = 'sensor_data.json'
                with open(filename, 'w') as json_file:
                    json.dump([sensor_data.__dict__], json_file)
                # 웹 서버로 데이터 전송
                #send_to_server(server_url, sensor_data.__dict__)
                
            elif control == 1 :
                #select_num = input("which 1~4 LED : ")
                #if select_num == 1 :
                led_status = not led_status
                GPIO.output(led_pin_1, GPIO.HIGH if led_status else GPIO.LOW)

            elif control == 2 :
                #select_num = input("which 1~4 Pump : ")
                #if select_num == 1 :
                pump_status = not pump_status
                GPIO.output(water_pump_pin_1, GPIO.HIGH if pump_status else GPIO.LOW)
    else :
        print("Auto Mode 0N")
        while True:
            try:
                data = client_socket.recv(1024)  # 클라이언트로부터 데이터를 받는다.
                if not data:
                    print("None Data")
                    break
                
                data_str = data.decode()
                sensor_id,temp_val, humi_val, light_val, Co2_Val, Soil_Val = map(float, data_str.split(','))
                
                # 센서 데이터 객체 생성
                sensor_data = SensorModule(sensor_id, light_val, temp_val, humi_val, Co2_Val, Soil_Val)
                """
                if sensor_id == 1:
                    if light_val > 500 :
                        GPIO.output(led_pin_1, GPIO.HIGH)
                    else :
                        GPIO.output(led_pin_1, GPIO.LOW)
                    if Soil_Val > 500 :  # 값 측정 필요
                        GPIO.output(water_pump_pin_1, GPIO.HIGH)
                    else :
                        GPIO.output(water_pump_pin_1, GPIO.LOW)

                
                elif sensor_id == 2:
                    if light_val > 500 :
                        GPIO.output(led_pin_2, GPIO.HIGH)
                    else :
                        GPIO.output(led_pin_2, GPIO.LOW)
                    if Soil_Val > 500 :  # 값 측정 필요
                        GPIO.output(water_pump_pin_2, GPIO.HIGH)
                    else :
                        GPIO.output(water_pump_pin_2, GPIO.LOW)
                """
                # 4번까지 추가 가능


                # 데이터를 JSON 파일에 저장
                filename = 'sensor_data.json'
                with open(filename, 'w') as json_file:
                    json.dump([sensor_data.__dict__], json_file)
    
                # 센서값 출력
                print("Farm ID : {}".format(int(sensor_data.id)))
                print("Temperature: {:.1f}°C, Humidity: {:.1f}%".format(sensor_data.tempVal, sensor_data.humiVal))
                print("Light Value:", int(sensor_data.lightVal))
                print("CO2: {} ppm".format(int(sensor_data.Co2Val)))
                print("Soil Moisture: {}".format(int(sensor_data.Co2Val)))
                
               
                # 웹 서버로 데이터 전송
                #send_to_server(server_url, sensor_data.__dict__)
    
                # 6초 대기
                sleep(6)
            except BrokenPipeError as e:
                print("BrokenPipeError", e)
            except ConnectionResetError as e:
                print("ConnectionResetError", e)
            except KeyboardInterrupt:
                GPIO.cleanup()
        client_socket.close()

server_socket.close()



"""
자동제어 부분 만들어야함
물펌프랑 조도

"""