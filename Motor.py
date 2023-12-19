import RPi.GPIO as GPIO
import numpy as np
import time

class PostureMapping: 
    def __init__(self) -> None:
        GPIO.setwarnings(False)
        
        # Set up servo_pins
        self.servo_1 = 10;
        self.servo_2 = 11;
        self.servo_3 = 12;
        self.servo_4 = 13;
        
        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_1, GPIO.OUT)
        GPIO.setup(self.servo_2, GPIO.OUT)
        GPIO.setup(self.servo_3, GPIO.OUT)                           
        GPIO.setup(self.servo_4, GPIO.OUT)

        # Create PWM instances as class attributes
        self.pwm_1 = GPIO.PWM(self.servo_1, 50)  # 50 Hz frequency
        self.pwm_2 = GPIO.PWM(self.servo_2, 50)
        self.pwm_3 = GPIO.PWM(self.servo_3, 50)
        self.pwm_4 = GPIO.PWM(self.servo_4, 50)
        
        # Set min/max duty cycle
        self.SERVO_MAX_DUTY = 12
        self.SERVO_MIN_DUTY = 3

        # Start PWM
        self.pwm_1.start(0)
        self.pwm_2.start(0)
        self.pwm_3.start(0)
        self.pwm_4.start(0)
        
    # Controlling two bottom servo at once 
    def set_angle_1(self, duty1):
        # for i in range(start_angle, desired_angle, time):
        # duty1 = self.SERVO_MIN_DUTY+(desired_angle*(self.SERVO_MAX_DUTY-self.SERVO_MIN_DUTY)/270.0)
        # duty2 = (self.SERVO_MAX_DUTY + self.SERVO_MIN_DUTY) - duty1
        
        print(duty1)

        GPIO.output(self.servo_1, True)
        GPIO.output(self.servo_2, True)
        self.pwm_1.ChangeDutyCycle(duty1)
        # self.pwm_2.ChangeDutyCycle(duty2)
        time.sleep(0.3)                   # Change this delay as needed. 
        GPIO.output(self.servo_1, False)
        GPIO.output(self.servo_2, False)
        self.pwm_1.ChangeDutyCycle(0)
        self.pwm_2.ChangeDutyCycle(0)
        
    def set_angle_2(self, duty1):
        # for i in range(start_angle, desired_angle, time):
        # duty1 = self.SERVO_MIN_DUTY+(desired_angle*(self.SERVO_MAX_DUTY-self.SERVO_MIN_DUTY)/270.0)
        # duty2 = (self.SERVO_MAX_DUTY + self.SERVO_MIN_DUTY) - duty1
        
        print(duty1)
        # duty2 = 15 - duty1

        GPIO.output(self.servo_3, True)
        GPIO.output(self.servo_4, True)
        self.pwm_3.ChangeDutyCycle(duty1)
        # self.pwm_4.ChangeDutyCycle(duty2)
        time.sleep(10.0)                   # Change this delay as needed. 
        GPIO.output(self.servo_3, False)
        GPIO.output(self.servo_4, False)
        self.pwm_3.ChangeDutyCycle(0)
        self.pwm_4.ChangeDutyCycle(0)
        
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    
    try:
        print("main is running")
        mapping = PostureMapping()
        # for i in np.arange(3, 12, 0.1):
        #     mapping.set_angle_2(i)
        mapping.set_angle_2(5.0)
        print("set angle to 0")
        time.sleep(1.0)
        # mapping.set_angle_1(90)
        # print("set angle to 90")
        # time.sleep(1.0)
        # mapping.set_angle_1(180)
        # print("set angle to 180")
        # time.sleep(1.0)
        
    except KeyboardInterrupt:
        mapping.cleanup()