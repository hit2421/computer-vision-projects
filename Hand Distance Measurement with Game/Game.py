import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Distance Mapping (Raw distance vs real-world distance in cm)
x_values = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y_values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x_values, y_values, 2)  # Polynomial fit: y = Ax^2 + Bx + C

# Game Variables
cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
timeStart = time.time()
totalTime = 20

# Main Loop
while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)  # Flip the image for a natural feel

    # Game Timer
    timeLeft = int(totalTime - (time.time() - timeStart))
    if timeLeft > 0:
        hands, _ = detector.findHands(img, draw=False)  # Returns list of hands

        if hands and isinstance(hands, list) and len(hands) > 0:
            hand = hands[0]
            if 'lmList' in hand and 'bbox' in hand:
                lmList = hand['lmList']
                x, y, w, h = hand['bbox']

                # Get key landmarks
                x1, y1 = lmList[5][:2]   # Base of index finger
                x2, y2 = lmList[17][:2]  # Base of pinky finger

                # Compute distance in pixels
                distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))

                # Convert pixel distance to cm
                A, B, C = coff
                distanceCM = A * (distance ** 2) + B * distance + C

                # Detect Hand Collision with Target
                if distanceCM < 40 and x < cx < x + w and y < cy < y + h:
                    counter = 1

                # Draw Bounding Box & Distance
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

        # Move Target on Hit
        if counter:
            counter += 1
            color = (0, 255, 0)  # Change color to green on hit
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (255, 0, 255)
                score += 1
                counter = 0

        # Draw Target Button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # Display Timer & Score
        cvzone.putTextRect(img, f'Time: {timeLeft}', (1000, 75), scale=3, offset=20)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)
    
    # Game Over Screen
    else:
        cvzone.putTextRect(img, 'Game Over', (400, 400), scale=5, offset=30, thickness=7)
        cvzone.putTextRect(img, f'Your Score: {score}', (450, 500), scale=3, offset=20)
        cvzone.putTextRect(img, 'Press R to restart', (460, 575), scale=2, offset=10)

    # Display Frame
    cv2.imshow("Image", img)
    
    # Handle Key Press
    key = cv2.waitKey(1)
    if key == ord('r'):  # Restart Game
        timeStart = time.time()
        score = 0

cap.release()
cv2.destroyAllWindows()
