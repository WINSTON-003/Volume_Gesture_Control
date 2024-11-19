
# Hand Tracking Involves Palm detection and Hand Landmarks
# For a hand there are 21 points detected


import cv2 as cv
import mediapipe as mp      # it has many tracking libraries
import numpy as np
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()         # click with ctrl on Hands to get definition
mpDraw = mp.solutions.drawing_utils

cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)


#For FPS
curr_time = 0
prev_time = 0

while (True):
    ret, frame = cap.read()
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)            # checking if hands are detected

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                #print(id, lm)      prints the landmark of all finger points
                h,w ,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)

                # if draw:           #To draw circle in particular landmark or fingerpoint
                #     cv.circle(frame, (cx, cy), 10, (255,125,24), -1)


            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    curr_time = time.time()
    fps = 1/(curr_time - prev_time)

    prev_time = curr_time
    fps = str(int(fps))                         #cnvrtng to string and rounding off, so we can display in frame

    cv.putText(frame, fps, (10, 70), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,0,0), 2)


    cv.imshow("image", frame)
    key = cv.waitKey(1) & 0xFF
    if key == 27:
        break






