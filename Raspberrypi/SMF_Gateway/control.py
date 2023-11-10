import RPi.GPIO as GPIO
from time import sleep

led_pin_1 = 6
led_pin_2 = 13
water_pump_pin_1 = 19
water_pump_pin_2 = 26
water_pump_pin_M = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_pin_1, GPIO.OUT)
GPIO.setup(led_pin_2, GPIO.OUT)
GPIO.setup(water_pump_pin_M, GPIO.OUT)
GPIO.setup(water_pump_pin_1, GPIO.OUT)
GPIO.setup(water_pump_pin_2, GPIO.OUT)

GPIO.output(led_pin_1, GPIO.HIGH)
GPIO.output(led_pin_2, GPIO.HIGH)
GPIO.output(water_pump_pin_1, GPIO.HIGH)
GPIO.output(water_pump_pin_2, GPIO.HIGH)
GPIO.output(water_pump_pin_M, GPIO.LOW)


led_status = [False,False,False,False]
pump_status = [False,False,False,False]
while True:
	control = int(input("select : ")) # 1. LED 2. Pump
	try :
		if control >= 3:
			continue
		while True :
			led_status,pump_status
			if control == 1 :
				select_num = int(input("which 1~2 LED : "))   # 3 is break
				if select_num == 1 :
					led_status[0] = not led_status[0]
					GPIO.output(led_pin_1, GPIO.LOW if led_status[0] else GPIO.HIGH)
				elif select_num == 2 :
					led_status[1] = not led_status[1]
					GPIO.output(led_pin_2,GPIO.LOW if led_status[1] else GPIO.HIGH)
				elif select_num == 3 :
					break
				print(led_status)

			elif control == 2 :
				select_num = int(input("which 1~2 Pump : "))
				if select_num == 1 :
					pump_status[0] = not pump_status[0]
					GPIO.output(water_pump_pin_1, GPIO.LOW if pump_status[0] else GPIO.HIGH)
				elif select_num == 2 :
					pump_status[1] = not pump_status[1]
					GPIO.output(water_pump_pin_2,GPIO.LOW if pump_status[1] else GPIO.HIGH)
				elif select_num == 3 :
					break
				
				if pump_status[0] and pump_status[1]:
					GPIO.output(water_pump_pin_M, GPIO.HIGH)
				elif pump_status[0] or pump_status[1]:
					GPIO.output(water_pump_pin_M, GPIO.HIGH)
				else:
					GPIO.output(water_pump_pin_M, GPIO.LOW)
				
				print(pump_status)
				print(pump_status[0] or pump_status[1])
		
	except ValueError:
		print("input only 1~2")
		continue
		
GPIO.cleanup()


