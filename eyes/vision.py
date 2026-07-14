import cv2 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from brain.mini_brain import MimicBrain

class Eyes:
    def __init__(self, brain:"MimicBrain"):
        self.brain = brain
        
        self.cap = cv2.VideoCapture(0)

        # Check if the webcam opened correctly
        if not self.cap.isOpened():
            print("Error: Could not open the camera.")
            exit()

        print("Camera accessed successfully. Press 'q' to quit.")

    def open_camera(self):

        while True:

            ret, frame = self.cap.read()

         
            if not ret:
                print("Error: Can't receive frame.")
                break

            cv2.imshow('Laptop Camera Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()