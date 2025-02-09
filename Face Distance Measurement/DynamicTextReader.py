import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

# Initialize webcam (use 0 if 2 doesn't work)
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

textList = ["Welcome to the madness, ", "Hitesh's School of Tech Wizardry!",
            "Where we *try* to teach", "Computer Vision,", "Robotics, and AI...",
            "but mostly end up debugging for hours.",
            "If this video made sense,", "Congrats, you're a genius!",  
            "If not, just Like, Share,", "and pretend it did!"]


sen = 25  # Sensitivity for text scaling

while True:
    success, img = cap.read()
    
    # Handle camera failure
    if not success:
        print("Failed to capture image")
        continue

    # Create a blank image for text overlay
    imgText = np.zeros_like(img, dtype=np.uint8)

    # Detect face mesh
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]

        # Calculate the width between two face landmarks
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3  # Approximate actual width of the face in cm

        # Camera focal length (predefined or calibrated)
        f = 840
        d = (W * f) / w  # Depth estimation
        print(f"Depth: {d:.2f} cm")

        # Display depth information on the screen
        cvzone.putTextRect(img, f'Depth: {int(d)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2, thickness=2, colorR=(0, 255, 0))

        # Dynamic text scaling based on depth
        for i, text in enumerate(textList):
            singleHeight = 20 + int((int(d / sen) * sen) / 4)
            scale = 0.4 + (int(d / sen) * sen) / 75
            cv2.putText(imgText, text, (50, 50 + (i * singleHeight)),
                        cv2.FONT_ITALIC, scale, (255, 255, 255), 2)

    # Stack images for display
    imgStacked = cvzone.stackImages([img, imgText], 2, 1)
    cv2.imshow("Image", imgStacked)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
