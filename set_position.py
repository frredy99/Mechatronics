import time
import cv2
import mediapipe as mp


def get_distance(rgb_image, detection_result):
    image = cv2.cvtColor(detection_result, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        # 어깨 관절 좌표 가져오기
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # 좌표가 있는 경우에만 거리 계산
        if left_shoulder and right_shoulder:
            # 픽셀 좌표를 실제 거리로 변환
            width_pixels = abs(
                right_shoulder.x * image.shape[1] - left_shoulder.x * image.shape[1])
            distance = width_pixels

    """
    focal_length = 800  # 초점 거리
    known_width = 14.0  # 실제 사물의 가로 너비 (예: 센티미터 단위)
    perceived_width = 300  # 이미지상 사물의 가로 픽셀 너비

    distance = (known_width * focal_length) / perceived_width
    """
    return distance


def check_status():
    global status_maintained
    min_distance = 10
    max_distance = 30
    time_interval = 5
    elapsed_time = 0
    distance = get_distance()

    if (distance > max_distance):
        print("화면과의 거리가 너무 멉니다")
        status_maintained = False
    if (distance < min_distance):
        print("화면과의 거리가 가깝습니다")
        status_maintained = False
    if (distance > max_distance or distance < min_distance):
        print("화면과의 거리가 적절합니다")
        status_maintained = True


def start():
    # 작업을 수행할 최소 시간 간격 설정 (예: 5초)
    time_interval = 5  # 초 단위로 설정

    start_time = time.time()  # 현재 시간 기록

    while True:
        current_time = time.time()  # 현재 시간 기록
        elapsed_time = current_time - start_time  # 경과된 시간 계산

        # 일정 시간이 지나지 않았고 상태가 유지되었다면 계속해서 상태를 확인합니다.
        if elapsed_time < time_interval and status_maintained:
            check_status()

        # 일정 시간이 지나거나 상태가 변경되어 초기화해야 할 때
        if elapsed_time >= time_interval or not status_maintained:
            if not status_maintained:
                print("상태가 변경되어 시간 초기화")
            start_time = time.time()  # 현재 시간으로 다시 시작 시간 갱신
            # status_maintained = True
