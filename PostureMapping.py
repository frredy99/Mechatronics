
import numpy as np 


class PostureMapping: 
    def __init__(self) -> None:
        # For saving Current Angle
        # and initiating angle positions
        angle_1 = 0
        angle_2 = 0
        self.angle_1 = angle_1
        self.angle_2 = angle_2

        # Mapping Customizing
        self.optimum_shoulder_to_head = 70   # Set optimum angle for the mapping         
        self.count = 0  # Count the number of mapping iteration
        self.activated = False # Flag to indicate if PostureMapping is started
        self.count_threshold = 30 # Threshold for count
        self.classifier = 20  #(angle)                           
        self.large_mapping_rate = 0.5 # How much angle to change at once
        self.small_mapping_rate = 0.3 



    def Iterator(self, shoulder_to_head):
        
        # Compute loss
        # Change the the loss function if needed: squared 
        loss = shoulder_to_head - self.optimum_shoulder_to_head

        # Classifying type of mapping(lage/small scale) by the shoulder_to_head angle 
        # Mapping in Large Scale
        if np.abs(loss) >= self.classifier \
            and self.count <= self.count_threshold :
            
            try:
                del_angle2 = - self.large_mapping_rate * np.sign(loss)
            except Exception as e:
                print(f"Error 1: {e}")
            try:
                self.angle_2 += del_angle2
            except Exception as e:
                print(f"Error 2: {e}")
            self.count += 1
            return self.angle_1, self.angle_2, self.activated
        
        # Mapping in Small Scale
        elif self.classifier >= np.abs(loss) \
            and self.count <= self.count_threshold: 
            
            del_angle1 = - self.small_mapping_rate * np.sign(loss)
            self.angle_1 += del_angle1
            self.angle_2 -= del_angle1
            self.count += 1
            return self.angle_1, self.angle_2, self.activated

        else: 
            self.count = 0
            print(f"Now in correct posture! The angle is {shoulder_to_head}.")
            self.activated = False
            return self.angle_1, self.angle_2, self.activated