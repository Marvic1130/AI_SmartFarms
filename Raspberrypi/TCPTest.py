import socket
import RPi.GPIO as GPIO

BUTTON_PIN = 18
HOST = '0.0.0.0'  # 서버의 IP 주소.
PORT = 8888  # 서버에서 사용할 포트 번호.
ledOnOff = True

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 버튼 입력 처리 함수
def button_callback(channel):
    global ledOnOff
    print("Button pressed!")
    if ledOnOff:
        ledOnOff = False
    else:
        ledOnOff = True
    print("Now button state is", ledOnOff)

print('TCP Server Listening at', HOST, PORT)
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback, bouncetime=200)

while True:
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    
    while True:
        try:
            data = client_socket.recv(1024)  # 클라이언트로부터 데이터를 받는다.
            if not data:
                break
            
            print('Received from', addr, data.decode())
            client_socket.send(str(ledOnOff).encode())  # LED 버튼 상태 반환
        except BrokenPipeError as e:
            print("BrokenPipeError", e)

        except ConnectionResetError as e:
            print("ConnectionResetError", e)
            

    client_socket.close()
