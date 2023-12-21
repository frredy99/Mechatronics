import bluetooth
import struct

def send_data(data1, data2, target_address):
    port = 1

    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((target_address, port))
        
        data1 = struct.pack('f', data1)
        sock.send(data1)
        print(f"Data sent: {data1}")
        
        data2 = struct.pack('f', data2)
        sock.send(data2)
        print(f"Data sent: {data2}")
        
        sock.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_address = "D8:3A:DD:29:9A:A8"
    data_to_send1 = 6
    data_to_send2 = 7

    send_data(data_to_send1, data_to_send2, target_address)
