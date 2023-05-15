
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time

# 팬 모터에 사용할 GPIO 핀 번호 설정
PIN = 17

state = False

# GPIO 핀 번호 모드 설정
GPIO.setmode(GPIO.BCM)
# GPIO 핀을 출력 모드로 설정
GPIO.setup(PIN, GPIO.OUT)

# LCD 초기화 및 설정
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=16, rows=2)
lcd.clear()

# 팬 모터 제어 함수
def control_fan_motor(on):
    if on:
        GPIO.output(PIN, GPIO.HIGH) # 모터 켜기
    else:
        GPIO.output(PIN, GPIO.LOW) # 모터 끄기

# 팬 모터 켜기
control_fan_motor(False) # 초기 상태는 모터를 끄도록 설정

while True:
    if state:
        lcd.write_string("Fan ON")
    else:
        lcd.write_string("Fan OFF")
    user_input = input("팬 모터 제어 (on/off): ")
    if user_input.lower() == "on":
        control_fan_motor(True)
        state = True
    elif user_input.lower() == "off":
        state = False
    else:
        print("유효하지 않은 입력입니다. 다시 입력해주세요.")
        continue
    control_fan_motor(state)

    time.sleep(1) # 1초의 딜레이
    lcd.clear()
