import RPi.GPIO as GPIO
import time

# GPIO 모드 설정 (BCM 모드 사용)
GPIO.setmode(GPIO.BCM)

# 서보모터를 제어할 GPIO 핀 번호
servo_pin = 18

# GPIO 핀 설정 (출력으로 설정)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM 객체 생성 (핀 번호, 주파수)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz의 주파수로 PWM 생성

# 서보모터 각도를 PWM 신호로 변환하는 함수
def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2.5  # 0도는 2.5% duty cycle, 180도는 12.5% duty cycle
    return duty_cycle

try:
    while True:
        # 사용자로부터 각도 입력 받기
        angle = int(input("서보모터 각도를 입력하세요 (0~180): "))

        # 입력 받은 각도로 서보모터를 제어
        pwm.start(angle_to_duty_cycle(angle))
        print("{}도로 서보모터 제어".format(angle))
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    # 프로그램 실행 중에 Ctrl+C를 누르면 KeyboardInterrupt 예외가 발생하여 프로그램 종료
    pass

finally:
    # PWM 객체 정지 및 GPIO 설정 초기화
    pwm.stop()
    GPIO.cleanup()
