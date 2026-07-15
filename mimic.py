
from typing import TYPE_CHECKING
from helpers import prompts,helpers
import time
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
    
    
    def process(self, text:str):
        try:
            known_words = self.brain.get_brain()['words']
            prompt = self.prompts.agent_purpose(known_words=known_words)
            
            response = self.agent._genrate(text=text, system_prompt=prompt)
            
            if not response or not isinstance(response, dict) or not response.get("content"):
                print(f"""[LEVEL 5 ERROR] The agent response didnt respond in a valid format.
                                
                                \u2022 TYPE: {type(response)}\n
                                \u2022 CONTENT: {response or "Response is broken and can not be added"}\n
                                \u2022 length: {len(response) or "Can not be found"}\n
                                
                                """)
                self.voice.say(text)
                return True
                
            self.talking_process(response['content'])
            self.brain.add_guess(response.get("logic", ""))
            return True
        
        except Exception as ex:
            print(f"ERROR DURING MIMIC PROCESS: \n\t\u2022 {ex}")
            return False
        
    
    def hearing_process(self, silence_timeout:float=1.5, energy_threshold:int=400, wait_for_call:bool=True):
        if wait_for_call:
            heard = self.ears.wait_for_wake_word()
            if heard == "random":
                self.voice.say_something_random()
                return "random" # returns 'random' to alert a random word was said
            
            if heard is True:
                return self.__listen_and_save(silence_timeout=silence_timeout, energy_threshold=energy_threshold)
        
        return self.__listen_and_save(silence_timeout=silence_timeout, energy_threshold=energy_threshold)
                   
    def __listen_and_save(self, silence_timeout, energy_threshold):
        
        what_was_heard:str = self.ears.sr_listen(silence_timeout=silence_timeout, 
                                                dynamic_energy=energy_threshold)
        if not what_was_heard:
                return ''
            
        self.brain.save_new_word_or_sentance(what_was_heard)
        find_favorite, word = self.brain.find_favorite_word(words_heard=what_was_heard.strip().split())
        if find_favorite and word:
                self.talking_process(f"me like word '{word}'")
                time.sleep(1)
        return what_was_heard
    
    def talking_process(self, agent_response:str):
        self.voice.say(text=agent_response)