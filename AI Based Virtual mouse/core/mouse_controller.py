import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math
from .screenshot_capture import take_screenshot  # Relative import

import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Screen size
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Smoothening
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 10  # Increased smoothening factor for smoother movement

# Time for click cooldown
click_time = 0

def find_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def fingers_up(landmarks):
    fingers = []

    # Thumb
    if landmarks[4][0] > landmarks[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for tip in [8, 12, 16, 20]:
        if landmarks[tip][1] < landmarks[tip - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def start_mouse_control():
    global plocX, plocY, clocX, clocY, click_time

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = img.shape
                    lm_list.append((int(lm.x * w), int(lm.y * h)))

                if lm_list:
                    x1, y1 = lm_list[8]  # Index finger tip
                    x2, y2 = lm_list[4]  # Thumb tip

                    fingers = fingers_up(lm_list)

                    # Draw Hand Landmarks on the image
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Move Mouse (Fixed X-axis flip issue)
                    if fingers[1] == 1 and fingers[2] == 0:  # Index finger up, others down
                        x3 = np.interp(x1, (100, 540), (0, screen_width))  # Direct x-axis control
                        y3 = np.interp(y1, (100, 380), (0, screen_height))  # y-axis control

                        # Smooth movement calculation
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        pyautogui.moveTo(clocX, clocY)  # Updated mouse move
                        plocX, plocY = clocX, clocY

                    # Left Click (Thumb and index finger up)
                    if fingers[1] == 1 and fingers[0] == 1:
                        distance = find_distance(lm_list[8], lm_list[4])
                        if distance < 40:
                            if time.time() - click_time > 1:
                                pyautogui.click()
                                engine.say('Left Click')
                                engine.runAndWait()
                                click_time = time.time()

                    # Right Click (Index, middle finger up, others down)
                    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                        if time.time() - click_time > 1:
                            pyautogui.rightClick()
                            engine.say('Right Click')
                            engine.runAndWait()
                            click_time = time.time()

                    # Scroll (All fingers up)
                    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                        pyautogui.scroll(20)

                    # Screenshot (No fingers up)
                    if fingers == [0, 0, 0, 0, 0]:
                        if time.time() - click_time > 1:
                            take_screenshot()
                            engine.say('Screenshot Taken')
                            engine.runAndWait()
                            click_time = time.time()

        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
