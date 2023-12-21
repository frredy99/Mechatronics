import bluetooth

def receive_data():
    port = 1

    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", port))
        server_sock.listen(1)

        print("Waiting for connection...")
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")

        data = client_sock.recv(1024)
        print(f"Received data: {data.decode()}")

        client_sock.close()
        server_sock.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    receive_data()
