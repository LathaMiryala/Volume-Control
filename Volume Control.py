import cv2
import mediapipe as mp
import pyautogui
import math

x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    _, image = webcam.read()
    frame_height, frame_width, _ = image.shape
    image = cv2.flip(image, 1)  # Flip for mirror view
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger tip
                    cv2.circle(image, (x, y), 8, (0, 255, 255), 3)
                    x1, y1 = x, y
                if id == 4:  # Thumb tip
                    cv2.circle(image, (x, y), 8, (0, 255, 255), 3)
                    x2, y2 = x, y

            # Compute Euclidean distance
            dist = math.hypot(x2 - x1, y2 - y1)
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

            # Volume control logic
            if dist > 50:
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")

    cv2.imshow("Hand Volume Control using Python", image)

    if cv2.waitKey(10) == 27:  # ESC to exit
        break

webcam.release()
cv2.destroyAllWindows()
ghfahga
