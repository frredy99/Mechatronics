import pigpio
import time
import numpy as np
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

        data1 = client_sock.recv(4)
        data2 = client_sock.recv(4)
        
        data1 = struct.unpack('f', data1)[0]
        data2 = struct.unpack('f', data2)[0]
        print(f"Received data: {data1}, {data2}")

        client_sock.close()
        server_sock.close()
        
        return data1, data2
    except Exception as e:
        print(f"Error: {e}")

class MotorControl:
    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        self.pi = pigpio.pi()
        self.current_angle = 0
        self.timestamp = 0.1
        self.vel = 30       # degree/sec
        
        # initializing
        self.pi.set_servo_pulsewidth(self.servo_pin, 500)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        
    def set_angle(self, angle):
        MAX_DUTY = 2500
        MIN_DUTY = 500
        
        if angle > self.current_angle:
            timestamp = self.timestamp
        else:
            timestamp = -self.timestamp
        
        for i in np.arange(self.current_angle, angle, timestamp):
            duty_cycle = int((i / 180.0) * (MAX_DUTY-MIN_DUTY) + MIN_DUTY)
            self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
            time.sleep(self.timestamp/self.vel)
            
            
        
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        self.current_angle = angle
        
    def cleanup(self):
        self.pi.stop()
    
    
if __name__ == "__main__":
    print("main is running")
    
    servo1 = MotorControl(18)
    servo2 = MotorControl(17)
    
    while True:
        angle1, angle2 = receive_data()
        try:
            print("setting angle...")
            servo1.set_angle(angle1)
            servo2.set_angle(angle2)
            print("Done: ", servo1.current_angle, servo2.current_angle)
        
        except KeyboardInterrupt:
            servo1.cleanup()
            servo2.cleanup()
            print("servo cleaned up")

