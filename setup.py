
from typing import TYPE_CHECKING
from helpers import prompts,helpers
if TYPE_CHECKING:
    from brain.mini_brain import MimicBrain
    from voicebox import listen, speak



class Mimic:
    def __init__(self, 
                 brain:"MimicBrain", 
                 voicebox:"speak.Voice", 
                 ears:"listen.Ears", 
                 agent:"helpers.Helpers",
                 eyes=None) -> None:
        
        self.prompts = prompts.Prompts()
        self.agent = agent
        self.brain = brain
        self.voice = voicebox
        self.ears = ears
    
    def process(self, text:str=""):
        prompt = self.prompts.validate_text
        response = self.agent._genrate(text=text, system_prompt=prompt)
        self.talking_process(response)
        
    
    def hearing_process(self, silence_timeout:float=1.5, energy_threshold:int=400):
        
        what_was_heard = self.ears.sr_listen(silence_timeout=silence_timeout, 
                                             energy_threshold=energy_threshold)
        if not what_was_heard:
            return ""
        
        self.brain.save_new_word_or_sentance(what_was_heard)
        find_favorite, word = self.brain.find_favorite_word()
        if find_favorite and word:
            self.talking_process(f"me like word '{word}'")
        return what_was_heard
    
    def talking_process(self, text:str):
        self.voice.say(text=text)