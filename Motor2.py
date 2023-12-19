import pigpio
import time

class MotorControl:
    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        self.pi = pigpio.pi()
        
    def set_angle(self, angle):
        MAX_DUTY = 2000
        MIN_DUTY = 500
        duty_cycle = int((angle / 180.0) * MAX_DUTY + MIN_DUTY)
        self.pi.set_servo_pulsewidth(self.servo_pin, duty_cycle)
        time.sleep(10)
        self.pi.set_servo_pulsewidth(self.servo_pin, 0)
        
    def cleanup(self):
        self.pi.stop()
    
    
if __name__ == "__main__":
    print("main is running")
    
    servo1 = MotorControl(18)
    
    try:
        servo1.set_angle(90)
        print("setting angle")
        time.sleep(1)
    
    except KeyboardInterrupt:
        pass

    finally:
        servo1.cleanup()
        print("servo cleaned up")

