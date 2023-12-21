import pigpio
import time
import numpy as np
import bluetooth
import struct
import threading
import select

class MotorControl:
    pi = pigpio.pi()

    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        self.current_angle = 0
        self.timestamp = 0.1
        self.vel = 30  # degree/sec
        self.MAX_DUTY = 2400
        self.MIN_DUTY = 500
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        self.lock = threading.Lock()
        
    def initialize_angle(self, angle):
        duty_cycle = int((angle / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
        self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
        self.current_angle = angle
        time.sleep(1)

    def set_angle(self, angle):
        with self.lock:
            if angle > self.current_angle:
                timestamp = self.timestamp
            else:
                timestamp = -self.timestamp

            for i in np.arange(self.current_angle, angle, timestamp):
                duty_cycle = int((i / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
                time.sleep(self.timestamp / self.vel)

            # self.pi.set_servo_pulsewidth(self.servo_pin, 0)
            self.current_angle = angle

    def hold(self):
        with self.lock:
            duty_cycle = int((self.current_angle / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
            self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
            # time.sleep(0.01)

    @classmethod
    def cleanup(cls):
        cls.pi.stop()

def receive_data(timeout=0.33):
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

        try:
            client_sock, client_info = server_sock.accept()
            print(f"Accepted connection from {client_info}")

            data1 = client_sock.recv(4)
            data2 = client_sock.recv(4)
        except Exception as e:
            print(f"Error getting data: {e}")

        if not data1 or not data2:
            print("Failed to receive data. Maintaining current angle.")
            return None, None

        data1 = struct.unpack('f', data1)[0]
        data2 = struct.unpack('f', data2)[0]
        print(f"Received data: {data1}, {data2}")

        client_sock.close()
        server_sock.close()

        return data1, data2
    except KeyboardInterrupt:
        MotorControl.cleanup()
        return None, None

def control_servos():
    servo1 = MotorControl(14)
    servo2 = MotorControl(15)
    servo3 = MotorControl(17)
    servo4 = MotorControl(18)
    
    servo1.initialize_angle(170)
    servo2.initialize_angle(12)
    servo3.initialize_angle(0)
    servo4.initialize_angle(180)

    try:
        while True:
            angle1, angle2 = receive_data()
            try:
                if angle1 is not None and angle2 is not None:
                    print("setting angle...")
                    thread1 = threading.Thread(target=servo1.set_angle, args=(182-angle1,))
                    thread2 = threading.Thread(target=servo2.set_angle, args=(angle1,))
                    thread3 = threading.Thread(target=servo3.set_angle, args=(angle2,))
                    thread4 = threading.Thread(target=servo4.set_angle, args=(180-angle2,))

                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()

                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()

                    print("Done: ", servo2.current_angle, servo3.current_angle)
                else:
                    print(servo2.current_angle, servo3.current_angle)
                    thread1 = threading.Thread(target=servo1.hold)
                    thread2 = threading.Thread(target=servo2.hold)
                    thread3 = threading.Thread(target=servo3.hold)
                    thread4 = threading.Thread(target=servo4.hold)

                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()

                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()

            except KeyboardInterrupt:
                raise

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up...")
        MotorControl.cleanup()
        print("servo cleaned up")

if __name__ == "__main__":
    try:
        print("main is running")
        control_servos()
    except KeyboardInterrupt:
        MotorControl.cleanup()
        print("servo cleaned up")
