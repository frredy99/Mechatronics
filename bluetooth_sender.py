import bluetooth

def send_data(data, target_address):
    port = 1

    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((target_address, port))

        sock.send(data.encode())
        print(f"Data sent: {data}")

        sock.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_address = "D8:3A:DD:29:9A:A8"
    data_to_send = "Hello, Raspberry Pi!"

    send_data(data_to_send, target_address)
