import socket
import RPi.GPIO as GPIO

led_button = 18
fan_button = 17
servo_button = 27
HOST = '0.0.0.0'  # 서버의 IP 주소.
PORT = 8888  # 서버에서 사용할 포트 번호.
ledState = True
fanState = True
servoState = True

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(fan_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 버튼 입력 처리 함수
def ledButtonCallback(channel):
    global ledState
    print("Led Button pressed!")
    if ledState:
        ledState = False
    else:
        ledState = True
    print("Now Led button state is", ledState)
    # msg = 'l0::'+ str(ledState)
    # client_socket.send(msg.encode())

def fanButtonCallback(channel):
    global fanState
    print("Fan Button pressed!")
    if fanState:
        fanState = False
    else:
        fanState = True
    print("Now Fan button state is", fanState)
    # msg = 'f::' + str(fanState)
    # client_socket.send(msg.encode())
    
def servoButtonCallback(channel):
    global servoState
    print("Fan Button pressed!")
    if servoState:
        servoState = False
    else:
        servoState = True
    print("Now Servo Motor button state is", servoState)
    # msg = 's::' + str(servoState)
    # client_socket.send(msg.encode())

print('TCP Server Listening at', HOST, PORT)
GPIO.add_event_detect(led_button, GPIO.RISING, callback=ledButtonCallback, bouncetime=200)
GPIO.add_event_detect(fan_button, GPIO.RISING, callback=fanButtonCallback, bouncetime=200)
GPIO.add_event_detect(servo_button, GPIO.RISING, callback=servoButtonCallback, bouncetime=200)

while True:
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    
    while True:
        try:
            data = client_socket.recv(1024)  # 클라이언트로부터 데이터를 받는다.
            if not data:
                break
            
            print('Received from', addr, data.decode())
            msg = 'l0::'+ str(ledState) + ', f::' + str(fanState) + ', s::' + str(servoState) + '\n'
            try:
                client_socket.send(msg.encode()) # LED 버튼 상태 반환
                print('Send Succece msg:', msg)
            except OSError as e:
                print(e)
                
        except BrokenPipeError as e:
            print("BrokenPipeError", e)

        except ConnectionResetError as e:
            print("ConnectionResetError", e)
            

    client_socket.close()
