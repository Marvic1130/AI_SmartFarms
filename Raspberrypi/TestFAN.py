
import RPi.GPIO as GPIO
import time

# 사용할 GPIO 핀 번호 설정
PIN = 17

# GPIO 핀 번호 모드 설정
GPIO.setmode(GPIO.BCM)
# GPIO 핀을 출력 모드로 설정
GPIO.setup(PIN, GPIO.OUT)

# 팬 모터 제어 함수
def control_fan_motor(on):
    if on:
        GPIO.output(PIN, GPIO.HIGH) # 모터 켜기
    else:
        GPIO.output(PIN, GPIO.LOW) # 모터 끄기

# 팬 모터 켜기
control_fan_motor(False) # 초기 상태는 모터를 끄도록 설정

while True:
    user_input = input("팬 모터 제어 (on/off): ")
    if user_input.lower() == "on":
        control_fan_motor(True)
    elif user_input.lower() == "off":
        control_fan_motor(False)
    else:
        print("유효하지 않은 입력입니다. 다시 입력해주세요.")
        continue

    time.sleep(1) # 1초의 딜레이
