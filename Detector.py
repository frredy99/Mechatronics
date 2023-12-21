import time

class TurtleNeckDetector:
    def __init__(self):
        self.calculated_angle = 0
        self.count = 0
        self.detected = False  # Flag to indicate if detector is started
        self.start_time = 0

        self.turtle_neck_threshold = 30 # Threshold for turtleneck recognition
        self.count_threshold = 30  # Threshold for count
        self.time_limit = 180  # 3 minutes time limit
        
        self.is_running = False     # is motor running
        
    def detect_turtle_neck(self, calculated_angle):
        if not self.detected:       # initializing start time
            self.start_time = time.time()
            self.detected = True
        
        elif self.count <= self.count_threshold \
            and not self.is_running:
            if calculated_angle <= self.turtle_neck_threshold :
                self.count += 1
            else:
                self.count = 0
        
        if self.count >= self.count_threshold \
            and time.time() - self.start_time <= self.time_limit:
            # print("Turtle neck detected!")
            self.is_running = True   # Notifying motor is running
            return True
        else:
            # print("Turtle neck not detected.")
            return False
