import numpy as np
import cv2 as cv
import time
import HandtrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#print(volume.GetMasterVolumeLevel())
volrange = volume.GetVolumeRange()

minvol = volrange[0]
maxvol = volrange[1]

cap = cv.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
cTime = 0
pTime = 0
vol = 0
volbar = 400
detector = htm.handDetector(min_det_con = 0.7)


while(True):
    ret, frame = cap.read()
    detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw = False)
    if len(lmlist) !=0:
        #print(lmlist[4],lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv.circle(frame, (x1, y1), 8, (255, 140,24), -1)
        cv.circle(frame, (x2, y2), 8, (255, 140, 24), -1)

        cv.line(frame, (x1,y1), (x2,y2), (255, 140, 24), 4, cv.LINE_AA)
        cv.circle(frame, (cx,cy), 8, (255, 140, 24), -1)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        if length <= 25:
            cv.circle(frame, (cx,cy), 8, (0,255,0), -1)

        # Hand range 25 - 315
        # vol range -65 - 0.

        vol = np.interp(length, [25, 250], [minvol, maxvol])
        volbar = np.interp(length, [25, 250], [400,150])
        print(vol)

        volume.SetMasterVolumeLevel(vol, None)

    cv.rectangle(frame, (50,150), (80, 400), (255, 0, 0), 3)
    cv.rectangle(frame, (50, int(volbar)), (80, 400), (255, 0, 0), cv.FILLED)


    if len(lmlist) != 0:
        print(lmlist[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)

    pTime = cTime
    fps = str(int(fps))  # cnvrtng to string and rounding off, so we can display in frame

    cv.putText(frame, fps, (10, 70), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 2)

    cv.imshow("image", frame)
    key = cv.waitKey(1) & 0xFF
    if key == 27:
        break