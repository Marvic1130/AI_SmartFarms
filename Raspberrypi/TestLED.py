import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


led_pin = 23

GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED ON")
        time.sleep(1)  

        GPIO.output(led_pin, GPIO.LOW)
        print("LED OFF")
        time.sleep(1)  

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
