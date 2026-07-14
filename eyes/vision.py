import cv2 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mini_brain import MimicBrain

class Eyes:
    def __init__(self, brain:"MimicBrain"):
        self.brain = brain