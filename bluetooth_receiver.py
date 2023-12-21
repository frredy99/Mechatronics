import bluetooth
import struct

def receive_data():
    port = 1

    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", port))
        server_sock.listen(1)

        print("Waiting for connection...")
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")
        
        while True:

            data1 = client_sock.recv(4)
            data2 = client_sock.recv(4)
            
            if not data1 or not data2:
                break
            
            data1 = struct.unpack('f', data1)[0]
            data2 = struct.unpack('f', data2)[0]
            print(f"Received data: {data1}, {data2}")

        client_sock.close()
        server_sock.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    receive_data()
