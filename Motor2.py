import pigpio
import time
import numpy as np
import bluetooth
import struct
import threading
import select

class MotorControl:
    pi = pigpio.pi()

    def __init__(self, servo_pin1, servo_pin2, servo_pin3, servo_pin4):
        self.servo_pin = [servo_pin1, servo_pin2, servo_pin3, servo_pin4]
        self.current_angle = [0, 0, 0, 0]
        self.timestamp = 0.1
        self.vel = 30  # degree/sec
        self.MAX_DUTY = 2400
        self.MIN_DUTY = 500
        self.pi.set_servo_pulsewidth(self.servo_pin[0], 0)
        self.pi.set_servo_pulsewidth(self.servo_pin[1], 0)
        self.pi.set_servo_pulsewidth(self.servo_pin[2], 0)
        self.pi.set_servo_pulsewidth(self.servo_pin[3], 0)
        self.lock = threading.Lock()
        
    def initialize_angle(self, pin_num, angle):
        duty_cycle = int((angle / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
        self.pi.set_servo_pulsewidth(self.servo_pin[pin_num], duty_cycle)
        self.current_angle[pin_num] = angle
        time.sleep(0.1)

    def set_angle(self, angle1, angle2):
        with self.lock:
            if angle1 > self.current_angle:
                timestamp1 = self.timestamp
            else:
                timestamp1 = -self.timestamp
            
            angle_step1 = np.arange(self.current_angle[0], angle1, timestamp1)
            angle_step2 = np.linspace(self.current_angle[2], angle2, len(angle_step1))
            for i in len(angle_step1):
                duty_cycle0 = int(((182-angle_step1[i]) / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                duty_cycle1 = int((angle_step1[i] / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                self.pi.set_servo_pulsewidth(self.servo_pin[0], duty_cycle0)
                self.pi.set_servo_pulsewidth(self.servo_pin[1], duty_cycle1)
                
                duty_cycle2 = int((angle_step2[i] / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                duty_cycle3 = int(((180-angle_step2[i]) / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                self.pi.set_servo_pulsewidth(self.servo_pin[2], duty_cycle2)
                self.pi.set_servo_pulsewidth(self.servo_pin[3], duty_cycle3)
                
                time.sleep(self.timestamp / self.vel)

            # self.pi.set_servo_pulsewidth(self.servo_pin, 0)
            self.current_angle = [182-angle1, angle1, angle2, 180-angle2]

    def hold(self):
        with self.lock:
            for i in range(4):
                duty_cycle = int((self.current_angle[i] / 180.0) * (self.MAX_DUTY - self.MIN_DUTY) + self.MIN_DUTY)
                self.pi.set_servo_pulsewidth(self.servo_pin[i], duty_cycle)
            time.sleep(0.02)

    @classmethod
    def cleanup(cls):
        cls.pi.stop()

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
    except KeyboardInterrupt:
        MotorControl.cleanup()
        return None, None

def control_servos():
    servo = MotorControl(14, 15, 17, 18)
    
    servo.initialize_angle(0, 170)
    servo.initialize_angle(1, 12)
    servo.initialize_angle(2, 0)
    servo.initialize_angle(3, 180)

    while True:
        angle1, angle2 = receive_data()
        try:
            if angle1 is not None and angle2 is not None:
                print("setting angle...")
                
                servo.set_angle(angle1, angle2)

                print("Done: ", servo.current_angle[1], servo.current_angle[2])
            else:
                print(servo.current_angle[1], servo.current_angle[2])
                
                servo.hold()

        except KeyboardInterrupt:
            MotorControl.cleanup()
            print("servo cleaned up")

if __name__ == "__main__":
    try:
        print("main is running")
        control_servos()
    except KeyboardInterrupt:
        MotorControl.cleanup()
        print("servo cleaned up")
