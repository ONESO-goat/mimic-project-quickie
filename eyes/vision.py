import cv2 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from brain.mini_brain import MimicBrain

class Eyes:
    """
    
    For now, if I have the time and resources just add a eye contact detector.
    If the user looks into the camera, the "mimic" wakes up and starts talkings
    
    """
    def __init__(self):
       
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
    
    def detect_eye_contact(self):
        pass
        
if __name__ in "__main__":
    eyes = Eyes()