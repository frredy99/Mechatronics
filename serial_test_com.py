import bluetooth

server_mac_address = '50:C2:E8:1B:18:BE'  # 라즈베리 파이 블루투스 MAC 주소 입력
port = 1    # 포트는 임의로 작성하기
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_mac_address, port))

# 라즈베리파이 serail 통신
data_to_send = "(duty_1, duty_2)"
sock.send(data_to_send)
