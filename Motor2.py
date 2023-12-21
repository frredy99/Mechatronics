import pigpio
import time
import numpy as np

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
    
    while True:
        angle = float(input("input angle: "))
        try:
            print("setting angle...")
            servo1.set_angle(angle)
            print("Done: ", servo1.current_angle)
        
        except KeyboardInterrupt:
            servo1.cleanup()
            print("servo cleaned up")

