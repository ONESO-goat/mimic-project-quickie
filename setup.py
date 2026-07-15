from mimic import Mimic
from brain.mini_brain import MimicBrain
from voicebox.listen import Ears
import time
from voicebox.speak import Voice
from helpers.helpers import Helpers

def setup_mimic() -> Mimic:
    brain = MimicBrain()
    ears = Ears()
    voice = Voice(brain=brain, language="english", perferred_tts="pyttsx3")
    agent = Helpers(ai_to_use="gemini")
    
    mimic = Mimic(brain=brain, voicebox=voice, ears=ears, agent=agent)
    return mimic

def main(wait_for_call:bool=True):
    mimic = setup_mimic()
    while True:
        time.sleep(1)
        heard_text = mimic.hearing_process(silence_timeout=1.5, energy_threshold=400, wait_for_call=wait_for_call)
        if heard_text == "random" or not heard_text:
            continue
        
        if heard_text:
            mimic.process(heard_text)
            
            
if __name__ == "__main__":

    main(False)