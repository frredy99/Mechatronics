import bluetooth

# serial 통신 관련
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1  # 사용할 포트 번호 (라즈베리 파이에서 수신 대기할 포트)

server_socket.bind(('', port))
server_socket.listen(1)

client_sock, address = server_socket.accept()
print("Connected to", address)

# serial 통신 관련
data = client_sock.recv(1024)
print("Received:", data.decode())
