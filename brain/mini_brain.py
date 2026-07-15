import json
from helpers.config import Config
import copy
from datetime import datetime, timezone
import random

class MimicBrain:
    def __init__(self):
        self.brain = self.get_brain()
        self.chat_history = self.get_chat_history()
        self.recent_memory = []
        self.favorite_word = ""
    
    def get_chat_history(self):
        try:
            with open(Config.chat_history_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as ex:
            raise ValueError(f"Error occured during json process: {ex}")
        
    def get_brain(self)->dict:
        try:
            with open(Config.brain_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as ex:
            raise ValueError(f"Error occured during json process: {ex}")
        
    def save_new_word_or_sentance(self, text:str):
        text = text.lower().strip()
        if not text:
            return
        brain = copy.deepcopy(self.brain)
        
        text_len = len(text.split())
        if text_len == 1:
            if text not in self.brain['words']:
                brain['words'].append(text)
                       
        if text_len > 1 and text_len <= 15:
            if text not in self.brain['phrase']:
                brain['phrase'].append(text)
                brain = self.loop_new_words(brain=brain, text=text)
                
        elif text_len > 15 and text_len <= 20:
            if text not in self.brain['sentence']:
                brain['sentence'].append(text)
                brain = self.loop_new_words(brain=brain, text=text)
            
        else:
            brain = self.loop_new_words(brain=brain, text=text)
            
        if brain != self.brain:
            self.save_to_brain(brain)
    
    def loop_new_words(self, brain, text:str):
     
        for word in text.split():
            if word not in brain['words']:
            
                brain['words'].append(word)
        return brain
    
    def add_guess(self, guess:str):
        if not guess:
            return
        brain = copy.deepcopy(self.brain)
        brain["logic"]['guesses'].append(guess)
        self.save_to_brain(brain)
        
    def save_to_brain(self, data:dict):
        with open(Config.brain_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.brain = self.get_brain()
            
    def find_favorite_word(self, words_heard:list[str])->tuple[bool, str]:
        """
        Returns:
            tuple[bool, str]: Checks if a word was added, string is the word that was added to favorites
        """
        chance = random.randint(1, 100)
        if len(self.brain['favorite_words']) > 3 and chance == 67:

            if words_heard: 
                word = random.choice(words_heard)
                self.favorite_word = word
                if word not in self.brain['favorite_words']:
                    self.brain['favorite_words'].append(word)
                
                # Only save when changes are actually made
                self.save_to_brain(self.brain)
            return True, word
        else:
            chance = random.randint(1, 171547)
            if chance == 67: # chances of having a favorite word
                if words_heard: 
                    word = random.choice(words_heard)
                    self.favorite_word = word
                    if word not in self.brain['favorite_words']:
                        self.brain['favorite_words'].append(word)
                    
                    # Only save when changes are actually made
                    self.save_to_brain(self.brain)
                    return True, word
            
        return False, ""
    
    def create_chat_log(self, user_text:str, ai_response:dict):
        import uuid
        return {
            "id": str(uuid.uuid4()),
            "user": user_text,
            "response": ai_response,
            "timestamp": datetime.now(tz=timezone.utc).isoformat()
        }
        
    def save_chat_history(self, chat):
        history = self.get_chat_history()
        history.append(chat)
        with open(Config.chat_history_file, 'w') as f:
            json.dump(history, f, indent=4)
        
        self.chat_history = self.get_chat_history()   
        