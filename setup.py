from mimic import Mimic
from brain.mini_brain import MimicBrain
from voicebox.listen import Ears
from voicebox.speak import Voice
from helpers.helpers import Helpers

def setup_mimic() -> Mimic:
    brain = MimicBrain()
    ears = Ears()
    voice = Voice(brain=brain, language="english", perferred_tts="piper")
    agent = Helpers()
    
    mimic = Mimic(brain=brain, voicebox=voice, ears=ears, agent=agent)
    return mimic

def main():
    mimic = setup_mimic()
    while True:
        heard_text = mimic.hearing_process(silence_timeout=1.5, energy_threshold=400)
        if heard_text == "random" or not heard_text:
            continue
        
        if heard_text:
            mimic.process(heard_text)
            
            
if __name__ == "__main__":
    main()