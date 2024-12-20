import math 
import random  
import mediapipe
import cv2
import cvzone 
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(1) # For Selfie Camera
cap.set(3,800) # width
cap.set(4,600) # hight
detector = HandDetector(detectionCon = 0.7, maxHands = 1)

class SnakeGame:
    def __init__(self, pathFood):
        self.points = []
        self.length = []
        self.currentLength = 0
        self.allowedLenght = 100
        self.perviousHead = 0,0

        self.imageFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imageFood.shape

        self.foodPoints = 0, 0
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoints = random.randint(100, 600), random.randint(100, 400)

    def update(self, imgMain, currentHead):
        px, py = self.perviousHead
        cx, cy = currentHead
        self.points.append([cx,cy])
        distance = math.hypot(cx-px, cy-py)
        self.length.append(distance)
        self.currentLength += distance
        self.perviousHead = cx, cy
        #LENGTH REDUCATION
        if self.currentLength > self.allowedLenght:
            for i, lenght in enumerate(self.length):
                self.currentLength -= lenght
                self.length.pop(i)
                self.points.pop(i)
                if self.currentLength < self.allowedLenght:
                    break
        
        # EATING FOOD
        rx , ry = self.foodPoints
        if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry - self.hFood//2 < cy < ry + self.hFood//2:
           self.randomFoodLocation()
           self.allowedLenght +=25 

        # DRAW WORM
        if self.points:
            for i, points in enumerate(self.points):
                if i != 0 :
                    cv2.line(imgMain, self.points[i-1], self.points[i],(0,0,255),20)
                cv2.circle(imgMain, self.points[-1],20,(200,0,200),cv2.FILLED)

        # FOOD DRAWER 
        rx, ry = self.foodPoints
        imgMain = cvzone.overlayPNG(imgMain, self.imageFood,(rx-self.wFood//2, ry-self.hFood//2))

        return imgMain

game = SnakeGame('apple.png')
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img, flipType = False)

    if hands:
        lmList= hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        #cv2.circle(img,pointIndex,20,(200,0,200),cv2.FILLED)
        img = game.update(img,pointIndex)
    cv2.imshow("Snake Game [Python AI]", img)
    key= cv2.waitKey(1)