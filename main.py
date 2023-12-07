# -*- coding: utf-8 -*-
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import mediapipe as mp
from Angle import CalculateAngle

import RPi.GPIO as GPIO
import time

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


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the live stream mode:
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    try:
        annotated_image = draw_landmarks_on_image(output_image.numpy_view(), result)
        cv2.imshow('result', annotated_image)
        cv2.waitKey(33)    
        print(timestamp_ms, ":", CalculateAngle(result))
    except:
        print("failed to detect")
    pass

# Set up servo_pins
servo_1 = int(10);
servo_2 = int(11);

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_1, GPIO.OUT)


# Create PWM instance
pwm = GPIO.PWM(servo_1, 50)  # 50 Hz frequency

# Start PWM
pwm.start(0)

# Function to set servo angle
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_1, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_1, False)
    pwm.ChangeDutyCycle(0)

# Move servo to specific angle
set_angle(90)  # Move to 90 degrees

# Clean up GPIO
pwm.stop()
GPIO.cleanup()

model_file = open('pose_landmarker_full.task', 'rb')
model_data = model_file.read()
model_file.close()

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_buffer=model_data),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

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
        
        # Convert the frame received from OpenCV to a MediaPipe¡¯s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        
        # Send live image data to perform pose landmarking.
        # The results are accessible via the `result_callback` provided in
        # the `PoseLandmarkerOptions` object.
        # The pose landmarker must be created with the live stream mode.
        try:
            landmarker.detect_async(mp_image, timestamp)
        except:
            print('failed to detect')
        
        timestamp += 1
        
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    print("main is running.")