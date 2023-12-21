import pigpio
import time
import numpy as np
import bluetooth
import struct
import threading
import select

class MotorControl:
    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        self.pi = pigpio.pi()
        self.current_angle = 0
        self.timestamp = 0.1
        self.vel = 30       # degree/sec
        self.MAX_DUTY = 2400
        self.MIN_DUTY = 500
        
        # initializing
        self.pi.set_servo_pulsewidth(self.servo_pin, 500)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        
    def set_angle(self, angle):
        
        if angle > self.current_angle:
            timestamp = self.timestamp
        else:
            timestamp = -self.timestamp
        
        for i in np.arange(self.current_angle, angle, timestamp):
            duty_cycle = int((i / 180.0) * (self.MAX_DUTY-self.MIN_DUTY) + self.MIN_DUTY)
            self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
            time.sleep(self.timestamp/self.vel)
            
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        self.current_angle = angle
        
    def hold(self):
        duty_cycle = int((self.current_angle / 180.0) * (self.MAX_DUTY-self.MIN_DUTY) + self.MIN_DUTY)
        self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
        time.sleep(0.05)
        
    def cleanup(self):
        self.pi.stop()

def receive_data(timeout=0.1):
    port = 1

    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", port))
        server_sock.listen(1)

        print("Waiting for connection...")
        ready, _, _ = select.select([server_sock], [], [], timeout)

        if not ready:
            print("Timeout reached. Maintaining current angle.")
            return None, None

        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")

        data1 = client_sock.recv(4)
        data2 = client_sock.recv(4)

        if not data1 or not data2:
            print("Failed to receive data. Maintaining current angle.")
            return None, None

        data1 = struct.unpack('f', data1)[0]
        data2 = struct.unpack('f', data2)[0]
        print(f"Received data: {data1}, {data2}")

        client_sock.close()
        server_sock.close()

        return data1, data2
    except Exception as e:
        print(f"Error: {e}")
        return None, None
        
def control_servos():
    servo1 = MotorControl(18)
    servo2 = MotorControl(17)

    while True:
        angle1, angle2 = receive_data()
        try:
            if angle1 is not None and angle2 is not None:
                print("setting angle...")
                thread1 = threading.Thread(target=servo1.set_angle, args=(angle1,))
                thread2 = threading.Thread(target=servo2.set_angle, args=(angle2,))

                thread1.start()
                thread2.start()

                thread1.join()
                thread2.join()

                print("Done: ", servo1.current_angle, servo2.current_angle)
            else:
                print(servo1.current_angle, servo2.current_angle)
                thread1 = threading.Thread(target=servo1.hold)
                thread2 = threading.Thread(target=servo2.hold)

                thread1.start()
                thread2.start()

                thread1.join()
                thread2.join()

        except KeyboardInterrupt:
            servo1.cleanup()
            servo2.cleanup()
            print("servo cleaned up")
    
    
if __name__ == "__main__":
    print("main is running")
    control_servos()

