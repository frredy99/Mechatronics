import numpy as np

DTOR = 180/np.pi

class Angle:
    def __init__(self, landmarks_dic):
        self.landmarks_dic = landmarks_dic

    # get shoulder to head angle
    def CalculateShoulderToHeadAngle(self):

        center_shoulder = (self.landmarks_dic['left shoulder'] + self.landmarks_dic['right shoulder'])/2
        center_ear = (self.landmarks_dic['left ear'] + self.landmarks_dic['right ear'])/2
        
        angle_shoulder_ear = DTOR * np.arctan2(
            center_ear[1] - center_shoulder[1], center_ear[2] - center_shoulder[2])
        
        
        return angle_shoulder_ear

