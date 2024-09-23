# import cv2
# import numpy as np
# import dlib
# from imutils import face_utils

# def compute(ptA, ptB):
#     return np.linalg.norm(ptA - ptB)

# def blinked(a, b, c, d, e, f):
#     up = compute(b, d) + compute(c, e)
#     down = compute(a, f)
#     ratio = up / (2.0 * down)
#     if ratio > 0.25:
#         return 2  # Active
#     elif ratio > 0.21 and ratio <= 0.25:
#         return 1  # Drowsy
#     else:
#         return 0  # Sleeping

# def process_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     detector = dlib.get_frontal_face_detector()
#     predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#     sleep = 0
#     drowsy = 0
#     active = 0
#     status = ""
#     color = (255, 255, 255)  # Default color for text

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = detector(gray)

#         for face in faces:
#             landmarks = predictor(gray, face)
#             landmarks = face_utils.shape_to_np(landmarks)

#             left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
#             right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

#             if left_blink == 0 or right_blink == 0:
#                 sleep += 1
#                 drowsy = 0
#                 active = 0
#                 if sleep > 3:
#                     status = "Asleep"
#                     color = (255, 0, 0)
#             elif left_blink == 1 or right_blink == 1:
#                 sleep = 0
#                 active = 0
#                 drowsy += 1
#                 if drowsy > 4:
#                     status = "Sleepy"
#                     color = (0, 0, 255)
#             else:
#                 drowsy = 0
#                 sleep = 0
#                 active += 1
#                 if active > 6:
#                     status = "Awake"
#                     color = (0, 255, 0)

#             cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
#             for n in range(0, 68):
#                 (x, y) = landmarks[n]
#                 cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         yield frame_rgb, status

#     cap.release()
import cv2
import numpy as np
import dlib
from imutils import face_utils

def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    
    if ratio > 0.25:
        return 2, 100.0  # Active
    elif ratio > 0.21 and ratio <= 0.25:
        return 1, (0.25 - ratio) * 400  # Drowsy, return probability
    else:
        return 0, (0.21 - ratio) * 400  # Sleeping, return probability

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    sleep = 0
    drowsy = 0
    active = 0
    status = ""
    probability = 0
    color = (255, 255, 255)  # Default color for text

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink, left_prob = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink, right_prob = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if left_blink == 0 or right_blink == 0:
                sleep += 1
                drowsy = 0
                active = 0
                if sleep > 3:
                    status = "Asleep"
                    color = (255, 0, 0)
            elif left_blink == 1 or right_blink == 1:
                sleep = 0
                active = 0
                drowsy += 1
                if drowsy > 4:
                    status = "Sleepy"
                    color = (0, 0, 255)
            else:
                drowsy = 0
                sleep = 0
                active += 1
                if active > 6:
                    status = "Awake"
                    color = (0, 255, 0)

            # Combine the probabilities from both eyes
            probability = max(left_prob, right_prob)

            cv2.putText(frame, f"{status} ({probability:.1f}%)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield frame_rgb, status, probability

    cap.release()

