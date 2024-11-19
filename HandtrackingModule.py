
import cv2 as cv
import mediapipe as mp      # it has many tracking libraries
import numpy as np
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, model_complexity=1, min_det_con = 0.5,min_track_con = 0.5):         #initialization
        self.mode = mode                  #creating an object with own variable
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.min_det_con = min_det_con
        self.min_track_con = min_track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.min_det_con, self.min_track_con)  # click with ctrl on Hands to get definition
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw = True):

        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)            # checking if hands are detected

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo = 0, draw = True):

        lmlist = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                #print(id, lm)      #prints the landmark of all finger points
                h,w ,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmlist.append([id, cx, cy])

                if draw:           #To draw circle in particular landmark or fingerpoint
                    cv.circle(frame, (cx, cy), 10, (255,125,24), -1)

        return lmlist
def main():
    cap = cv.VideoCapture(0)

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    # For FPS
    curr_time = 0
    prev_time = 0

    detector = handDetector()

    while (True):
        ret, frame = cap.read()

        frame = detector.findHands(frame)
        lmlist = detector.findPosition(frame)
        if len(lmlist) != 0:
            print(lmlist[4])
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)

        prev_time = curr_time
        fps = str(int(fps))  # cnvrtng to string and rounding off, so we can display in frame

        cv.putText(frame, fps, (10, 70), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 2)

        cv.imshow("image", frame)
        key = cv.waitKey(1) & 0xFF
        if key == 27:
            break



if __name__ == "__main__":
    main()