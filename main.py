# -*- coding: utf-8 -*-
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import mediapipe as mp
from Angle import Angle
from Detector import TurtleNeckDetector
from PostureMapping import PostureMapping as pm

# To better demonstrate the Pose Landmarker API, we have created a set of visualization tools
# that will be used in this colab. These will draw the landmarks on a detect person, as well as
# the expected connections between those markers.
def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image


# returns x, y, z coordinates for nose, ears, and shoulders in dictionary
# {'nose': [x, y, z], 'left ear': [x, y, z], ...}
def get_coordinates(detection_result):
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
        
    return landmarks_dic


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# set global variable timestamp only when detected (need correction laters)
timestamp_detected = 0

# instantiate detector object
detector = TurtleNeckDetector()
posturemapping = pm()

# Create a pose landmarker instance with the live stream mode:
def callback(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global timestamp_detected
    try:
        annotated_image = draw_landmarks_on_image(output_image.numpy_view(), result)
        # if timestamp_detected == 0:     # when first detected
        #     detector.detected = True    # set detector flag true
        # cv2.imshow('result', annotated_image)
        # cv2.waitKey(33)
    except:
        print("failed to detect")
    try:
        landmarks_dic = get_coordinates(detection_result=result)
        angle = Angle(landmarks_dic)
        shoulder_to_head = angle.CalculateShoulderToHeadAngle()
        is_turtle_neck = detector.detect_turtle_neck(shoulder_to_head)
        print(f"{timestamp_detected}: {shoulder_to_head}, {is_turtle_neck}")
        
        # Initiating posture mapping process
        if is_turtle_neck:
            posturemapping.activated = True
            is_turtle_neck = False

        if posturemapping.activated:
            angle_1, angle_2, is_mapping_on = posturemapping.Iterator(shoulder_to_head)
            if not is_mapping_on:
                detector.is_running = False
            print(angle_1, angle_2)
            # Send the execution to the pi board
        
        timestamp_detected += 1
    except:
        print("failed to get angle")

# # Set up servo_pins
# servo_1 = int(10);
# servo_2 = int(11);

# # Set up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servo_1, GPIO.OUT)


# # Create PWM instance
# pwm = GPIO.PWM(servo_1, 50)  # 50 Hz frequency

# # Start PWM
# pwm.start(0)

# # Function to set servo angle
# def set_angle(angle):
#     duty = angle / 18 + 2
#     GPIO.output(servo_1, True)
#     pwm.ChangeDutyCycle(duty)
#     time.sleep(1)
#     GPIO.output(servo_1, False)
#     pwm.ChangeDutyCycle(0)

# # Move servo to specific angle
# set_angle(90)  # Move to 90 degrees

# # Clean up GPIO
# pwm.stop()
# GPIO.cleanup()

model_file = open('pose_landmarker_full.task', 'rb')
model_data = model_file.read()
model_file.close()

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_buffer=model_data),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=callback)

# For Video File input:
path = 0 # Input video path here
cap = cv2.VideoCapture(path)

# fps = cap.get(cv2.CAP_PROP_FPS)
# full_frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# output_height = 720
# output_width = int(output_height*original_width//original_height)

# Define the codec and create VideoWriter Object
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# out = cv2.VideoWriter('result.mp4', fourcc, fps, (output_width, output_height))

with PoseLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
    timestamp = 0
    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            # If loading a video, use 'break' instead of 'continue'.
            print(f"\nIgnoring empty camera frame\n")
            break
        
        # Convert the frame received from OpenCV to a MediaPipe¢®?s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        
        # Send live image data to perform pose landmarking.
        # The results are accessible via the `result_callback` provided in
        # the `PoseLandmarkerOptions` object.
        # The pose landmarker must be created with the live stream mode.
        
        landmarker.detect_async(mp_image, timestamp)
        
        timestamp += 1
        
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    print("main is running.")