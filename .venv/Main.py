import os
from cvzone.HandTrackingModule import HandDetector
import cv2

capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)

BGimg = cv2.imread("Resources/Background.png")

folder = "Resources/Modes"
ImgListd = os.listdir(folder)


ImgList = []
for imgmode in ImgListd:
    ImgList.append(cv2.imread(os.path.join(folder,imgmode)))
print(ImgList)

folderr = "Resources/Icons"

ImgListdd = os.listdir(folderr)
ImgListI = []
for imgmodee in ImgListdd:
    ImgListI.append(cv2.imread(os.path.join(folderr,imgmodee)))

mType = 0
selection = -1
counter = 0
selectspeed = 7
detector = HandDetector(detectionCon=0.8,maxHands = 1 )
Mpos = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
Selectionlist = [-1,-1,-1]

while  True:
    success, img = capture.read()
    hands, img = detector.findHands(img)

    BGimg[139:139+480,50:50+640] = img
    BGimg[0:720,847:1280] = ImgList[mType]


    if hands and counterPause==0 and mType<3:

        hand1 = hands[0]

        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0,1,0,0,0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0,1,1,0,0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0,1,1,1,0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection= -1
            counter = 0
        if counter >0:
            counter += 1
            print(counter)
            cv2.ellipse(BGimg,Mpos[selection-1],(103,103),0,0,counter*selectspeed,(0,255,0),20)
            if counter*selectspeed > 360:
                Selectionlist[mType] = selection
                mType +=1
                counter= 0
                selection = -1
                counterPause = 1


    if counterPause>0:
        counterPause +=1
        if counterPause>60:
            counterPause = 0

    if Selectionlist[0] != -1:
        BGimg[636:636 + 65, 133:133 + 65] = ImgListI[Selectionlist[0]-1]
    if Selectionlist[1] != -1:
        BGimg[636:636 + 65, 340:340 + 65] = ImgListI[2+Selectionlist[1]]
    if Selectionlist[2] != -1:
        BGimg[636:636 + 65, 542:542 + 65] = ImgListI[5+Selectionlist[2]]


    cv2.imshow("Background", BGimg)
    cv2.waitKey(1)