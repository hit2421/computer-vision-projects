import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

# Initialize webcam (change 2 to 0 if needed)
cap = cv2.VideoCapture(0)  
detector = FaceMeshDetector(maxFaces=1)

while True:
    success, img = cap.read()
    
    if not success:
        print("Failed to capture image")
        continue

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]

        # Calculate distance between the two points
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3  # Actual width in cm

        # Fixed Focal Length (adjust if needed)
        f = 840  
        d = (W * f) / w  # Depth calculation
        print(f"Depth: {d:.2f} cm")

        # Display depth on the image
        cvzone.putTextRect(img, f'Depth: {int(d)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2, thickness=2, colorR=(0, 255, 0))

    cv2.imshow("Image", img)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
