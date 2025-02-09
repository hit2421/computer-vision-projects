import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone

# Webcam Setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function
x_values = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y_values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x_values, y_values, 2)  # Quadratic fit: y = Ax^2 + Bx + C

# Loop
while True:
    success, img = cap.read()
    if not success:
        continue

    hands, _ = detector.findHands(img, draw=False)  # Returns list of hands and bbox info

    if hands and isinstance(hands, list) and len(hands) > 0:
        hand = hands[0]  # Ensure it is a dictionary
        if 'lmList' in hand and 'bbox' in hand:
            lmList = hand['lmList']
            x, y, w, h = hand['bbox']

            # Get finger landmarks
            x1, y1 = lmList[5][:2]   # Base of index finger
            x2, y2 = lmList[17][:2]  # Base of pinky finger

            # Calculate distance in pixels
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))

            # Convert distance to cm using polynomial fit
            A, B, C = coff
            distanceCM = A * (distance ** 2) + B * distance + C

            # Draw bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)

            # Display distance text
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Press 'q' to exit the loop

cap.release()
cv2.destroyAllWindows()
