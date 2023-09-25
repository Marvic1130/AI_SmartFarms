import socket
import serial
import time

# 서버 정보
HOST = '192.168.1.4'
PORT = 8080

# 소켓 초기화
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# USB 시리얼 포트 이름 설정
usb_port = '/dev/ttyUSB0'  # 위에서 확인한 포트 이름으로 변경

# 시리얼 포트 설정
ser = serial.Serial(usb_port, baudrate=115200, timeout=1)

try:
    while True:
        data = ser.readline().decode().strip()  # 시리얼 데이터 읽기 및 디코드
        values = data.split(',')
        
        # 빈 문자열을 제거하는 필터링 작업
        values = [val for val in values if val.strip()]
        
        if len(values) == 5:
            try:
                temp_val, humi_val, light_val, Co2_Val, Soil_Val = map(float, values)
                print(f"Received data: {data}")
                client_socket.sendall(data.encode())
            except ValueError:
                print(f"Invalid data format: {data}")
        else:
            print(f"Invalid data format: {data}")
        
        time.sleep(6)
        
except KeyboardInterrupt:
    ser.close()  # 시리얼 포트 닫기
