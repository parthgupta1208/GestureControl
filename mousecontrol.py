import cv2
import numpy as np
import cvzone.HandTrackingModule as htm
import pyautogui

wCam, hCam = 1920,1080
frameR = 0 
smoothening = 3
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(False,1,0.5,0.5)
wScr, hScr = pyautogui.size()[0],pyautogui.size()[1]
print(wScr, hScr)

while True:
    try:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        # print(lmList)
        if len(lmList) != 0:
            x1, y1 = lmList[8][0:2]
            x2, y2 = lmList[12][0:2]
            # print(x1, y1, x2, y2)
        fingers = detector.fingersUp()
        # cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) /smoothening
            clocY = plocY + (y3 - plocY) /smoothening
            pyautogui.moveTo(wScr - clocX*2, clocY*2)
            # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # if length > 40:
                # cv2.circle(img, (lineInfo[4], lineInfo[5]),
                # 15, (0, 255, 0), cv2.FILLED)
            pyautogui.click()
        
        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # if length > 40:
                # cv2.circle(img, (lineInfo[4], lineInfo[5]),
                # 15, (0, 255, 0), cv2.FILLED)
            pyautogui.rightClick()

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) /smoothening
            clocY = plocY + (y3 - plocY) /smoothening
            pyautogui.dragTo(wScr - clocX, clocY)
            # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
    except:
        pass
    # finally:
        # # cTime = time.time()
        # # fps = 1 / (cTime - pTime)
        # # pTime = cTime
        # # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
        # # 12. Display
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)