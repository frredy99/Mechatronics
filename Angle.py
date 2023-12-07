import numpy as np

DTOR = 180/np.pi

def CalculateAngle(detection_result):

    pose_landmarks_list = detection_result.pose_landmarks

    # nose, left ear, right ear, left shoulder, right shoulder
    idx_list = [0, 7, 8, 11, 12]
    
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]
    
    # get landmarks for nose, left ear, right ear, left shoulder, right shoulder
    landmarks_key = ['nose', 'left ear', 'right ear', 'left shoulder', 'right shoulder']
    landmarks_dic = {}
    for idx in range(len(idx_list)):
        try:
            landmark = pose_landmarks[idx_list[idx]]
        except:
            return "out of camera frame"
        landmarks_dic[landmarks_key[idx]] = np.array([landmark.x, 1 - landmark.y, -landmark.z])
    
    center_shoulder = (landmarks_dic['left shoulder'] + landmarks_dic['right shoulder'])/2
    center_ear = (landmarks_dic['left ear'] + landmarks_dic['right ear'])/2
    
    angle_shoulder_ear = DTOR * np.arctan2(
        center_ear[1] - center_shoulder[1], center_ear[2] - center_shoulder[2])
    
    
    return angle_shoulder_ear