# ssh pi@<your_raspberry_pi_ip_address> 
import RPi.GPIO as GPIO
import numpy as np 

############################################
###  Set the optimum angle for mapping   ###
############################################
optimum_theta_c = 70
optimum_theta_s = 15



class PostureMapping: 
    def __init__(self) -> None:

        # Set up servo_pins
        self.servo_1 = int(10);
        self.servo_2 = int(11);
        self.servo_3 = int(12);
        self.servo_4 = int(13);
        
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
    def set_angle_1(angle):
        duty1 = angle / 18 + 2          # Change this angle value as needed.
        duty2 = (180-angle) / 18 + 2    # Change this angle value as needed.
        GPIO.output(servo_1, True)
        GPIO.output(servo_2, True)
        self.pwm1.ChangeDutyCycle(duty)
        self.pwm2.ChangeDutyCycle(duty)
        time.sleep(1)                   # Change this delay as needed. 
        GPIO.output(servo_1, False)
        GPIO.output(servo_2, False)
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(duty)
    
    def set_angle_2(angle):
        duty3 = angle / 18 + 2          # Change this angle value as needed.
        duty4 = (180-angle) / 18 + 2    # Change this angle value as needed.
        GPIO.output(servo_3, True)
        GPIO.output(servo_4, True)
        self.pwm3.ChangeDutyCycle(duty)
        self.pwm4.ChangeDutyCycle(duty)
        time.sleep(1)                   # Change this delay as needed.
        GPIO.output(servo_3, False)
        GPIO.output(servo_4, False)
        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(duty)

    # Mapping Laptop to the optimum posture
    def Laptop(self, calculated_angle, epsilon=1e-1, maxIters=30):
        global optimum_theta_c  

        # Initialize Angle1 and Angle2
        angle_1 = 0
        angle_2 = 0

        # Change Angle1 and then Angle2
        for i in range(maxIters):
            
            self.set_angle_1(angle_1)
            angle_1 = angle_1 + 5          # The amount of angle1 change is 5 degree.

            # Checking the current state
            tolerance = optimum_theta_c - calculated_angle
            tolerance = tolerance * np.sign(tolerance)         # Changing the sign of tolerance
            if tolerance < epsilon:
                break
        
        for i in range(maxIters):

            self.set_angle_2(angle_2)
            angle_1 = angle_1 + 1          # The amount of angle2 change is 1 degree.

            # Checking the current state
            tolerance = optimum_theta_c - calculated_angle
            tolerance = tolerance * np.sign(tolerance)          # Changing the sign of tolerance
            if tolerance < epsilon:
                break

        # Clean up GPIO to reduce the load of the board.
        self.pwm_1.stop()
        self.pwm_2.stop()
        self.pwm_3.stop()
        self.pwm_4.stop()

        GPIO.cleanup()
        return "finnished"
       

    # Mapping iPad to the optimum posture
    def iPad(self): 
        pass
        
            

    