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
    
    while True:
        angle1 = float(input("input angle1: "))
        angle2 = float(input("input angle2: "))
        send_data(angle1, angle2, target_address)
