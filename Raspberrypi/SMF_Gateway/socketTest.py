import RPi_I2C_driver      # 라즈베리파이에서 LCD를 사용하기위한 라이브러리
import RPi.GPIO as GPIO    # 라즈베리파이에서 IN OUT 제어핀을 사용하기 위한 라이브러리
import tkinter as tk       # ?
from time import *         # delay역할의 sleep의 사용 라이브러리
import socket              # socket은 
import json
import requests
import random 

# 서버 정보
HOST = '0.0.0.0'  # 서버의 IP 주소.
PORT = 8080  # 서버에서 사용할 포트 번호.

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# 초기화
lcd = RPi_I2C_driver.lcd(0x27)  
switch_up = 17
switch_down = 27   

fan_pin = 5
servo_pin = 6
led_pin = 13
water_pump_pin = 19

lcd.backlight(0)

curr_scene = 0
curr_line = 0

# GPIO 초기화
GPIO.setmode(GPIO.BCM)  # GPIO핀을 BCM형식의 번호로 인식하기 위함?
GPIO.setwarnings(False)
GPIO.setup(switch_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fan_pin, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(water_pump_pin, GPIO.OUT)

GPIO.output(fan_pin, GPIO.LOW)
GPIO.output(led_pin, GPIO.LOW)
GPIO.output(water_pump_pin, GPIO.LOW)
pwm = GPIO.PWM(servo_pin, 50)

# status & value
# 현재 센서값은 임의의 값 출력을 위해서 값을 일단 넣은 상태 
# 이후 socket 통신으로 센서값을 받는 코드를작성하고 값을 변수에 받을 예정
# 0 = Non
light_val = 0
temp_val = 0
humi_val = 0
Co2_Val = 0
Soil_Val = 0

# actuator의 기본값 설정 이후 제어를 통해서 값을 변경하고 그값에따라 actuator 제어
fan_status = False
window_status = False
led_status = False
pump_status = False

# LCD 띄울 내용을 2차원 배열에 정리
Main_Scene_Text = [
    ["Mode    :", "Light   :", "Temp    :", "Humi    :"],
    ["Co2     :", "Soil    :", "Nan     :", "Nan     :"],
    ["Fan     :", "Motor   :", "RGB Bar :", "WPump   :"]
]

def set_angle(angle):
    duty_cycle = angle / 18.0 + 2.5  # 각도를 듀티 사이클로 변환
    pwm.ChangeDutyCycle(duty_cycle)  # 서보 모터 각도 설정
    sleep(0.3)  # 서보 모터가 제어를 받아야할 시간을 부여

# function
# callback함수로 만들어서 비동기처리를 할 수 있도록 구현
# 비동기처리? : 
def button_down_callback(channel):
    global curr_line,curr_scene
    curr_line+=1
    if curr_line == 4:
        curr_scene +=1
        if curr_scene > 2:
            curr_scene = 0
        curr_line = 0
    print_LCD()

def button_up_callback(channel):
    global curr_scene, curr_line
    global fan_status,window_status,led_status,pump_status
    global fan_pin,servo_pin,led_pin,water_pump_pin
    
    scene = curr_scene
    line = curr_line
    if scene == 2:
        if line == 0:
            fan_status = not fan_status
            GPIO.output(fan_pin, GPIO.HIGH if fan_status else GPIO.LOW)  # fan_pin을 켜거나 끕니다.
        elif line == 1:
            window_status = not window_status
            angle = 100 if window_status else 0     
            set_angle(angle)
        elif line == 2:
            led_status = not led_status
            GPIO.output(led_pin, GPIO.HIGH if led_status else GPIO.LOW)
        elif line == 3:
            pump_status = not pump_status
            GPIO.output(water_pump_pin, GPIO.HIGH if pump_status else GPIO.LOW)
    print_LCD()

def print_LCD():
    global curr_scene, curr_line
    global fan_status,window_status,led_status,pump_status
    
    arrow0 = ">" if curr_line == 0 else " "
    arrow1 = ">" if curr_line == 1 else " "
    arrow2 = ">" if curr_line == 2 else " "
    arrow3 = ">" if curr_line == 3 else " "
    
    if curr_scene == 0:
        lcd.lcd_display_string(arrow0+Main_Scene_Text[curr_scene][0] + "403", 1)
        lcd.lcd_display_string(arrow1+Main_Scene_Text[curr_scene][1] + "{:<8}".format("%d"   % light_val), 2)
        lcd.lcd_display_string(arrow2+Main_Scene_Text[curr_scene][2] + "{:<8}".format("%.1f"   % temp_val) , 3)
        lcd.lcd_display_string(arrow3+Main_Scene_Text[curr_scene][3] + "{:<8}".format("%.1f"   % humi_val), 4)
    elif curr_scene == 1:
        lcd.lcd_display_string(arrow0+Main_Scene_Text[curr_scene][0] + "{:<8}".format("%d"   % Co2_Val) , 1)
        lcd.lcd_display_string(arrow1+Main_Scene_Text[curr_scene][1] + "{:<8}".format("%d"   % Soil_Val), 2)
        lcd.lcd_display_string(arrow2+Main_Scene_Text[curr_scene][2] + "{:<8}".format("Nan") , 3)
        lcd.lcd_display_string(arrow3+Main_Scene_Text[curr_scene][3] + "{:<8}".format("Nan"), 4) 
    elif curr_scene == 2:    
        lcd.lcd_display_string(arrow0+Main_Scene_Text[curr_scene][0] + "{:<8}".format("ON" if fan_status else "OFF") , 1)
        lcd.lcd_display_string(arrow1+Main_Scene_Text[curr_scene][1] + "{:<8}".format("ON" if window_status else "OFF"), 2)
        lcd.lcd_display_string(arrow2+Main_Scene_Text[curr_scene][2] + "{:<8}".format("ON" if led_status else "OFF") , 3)
        lcd.lcd_display_string(arrow3+Main_Scene_Text[curr_scene][3] + "{:<8}".format("ON" if pump_status else "OFF"), 4)

def save_to_json(temperature, humidity,lightValue, co2Value, soilMoisture,pen,subMotor,LED,waterPump):
    data = {
        "lightValue": lightValue,
        "temperature": temperature,
        "humidity": humidity,
        "co2Value": co2Value,
        "soilMoisture": soilMoisture,
        "pen":pen,
        "subMotor":subMotor,
        "LED":LED,
        "waterPump":waterPump
    }
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    print("저장저장")

def read_json_data(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data
    
def send_to_server(url,data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)


def add_random_values():
    global light_val, temp_val, humi_val, Co2_Val, Soil_Val, data

    # 0부터 100 사이의 랜덤 값을 각 변수에 부여합니다.
    light_val = random.randint(0, 100)
    temp_val = random.randint(0, 100)
    humi_val = random.randint(0, 100)
    Co2_Val = random.randint(0, 100)
    Soil_Val = random.randint(0, 100)
    # data에 새로운 랜덤 값을 추가합니다.
    data = f"{light_val},{temp_val},{humi_val},{Co2_Val},{Soil_Val}"
    
    print(f"Updated data: {data}")
    sleep(2)  # 2초 대기

# intro
lcd.lcd_display_string("Hello 403",1)
lcd.lcd_display_string("Smart Farm",2)
sleep(2)
print_LCD()
pwm.start(0)

# Add event detect for the down button
GPIO.add_event_detect(switch_down, GPIO.RISING, callback=button_down_callback, bouncetime=1000)
GPIO.add_event_detect(switch_up, GPIO.RISING, callback=button_up_callback, bouncetime=1000)

# Loop 

while True:
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)

    while True:
        try:
            data = client_socket.recv(1024) # 클라이언트로부터 데이터를 받는다.
            if not data:
                print("None Data")
                break
            
            data_str = data.decode()    
            #add_random_values()
            temp_val, humi_val,light_val, Co2_Val, Soil_Val = map(float, data_str.split(','))

            save_to_json(temp_val, humi_val,light_val, Co2_Val, Soil_Val, fan_status, window_status, led_status, pump_status)
            # 각 센서값 출력
            print("Temperature: {:.1f}°C, Humidity: {:.1f}%".format(temp_val, humi_val))
            print("Light Value:", int(light_val))
            print("CO2: {} ppm".format(int(Co2_Val)))
            print("Soil Moisture: {}".format(int(Soil_Val)))
            server_url = 'https://smartfarmhansei.shop/senser/data'  # 웹 서버의 URL
            json_data = read_json_data('data.json')
            send_to_server(server_url, json_data)
            # 1초 대기
            sleep(6)
        except BrokenPipeError as e:
            print("BrokenPipeError", e)
        except ConnectionResetError as e:
            print("ConnectionResetError", e)
        except KeyboardInterrupt:
            GPIO.cleanup()
            lcd.clear()
    client_socket.close()

server_socket.close()
