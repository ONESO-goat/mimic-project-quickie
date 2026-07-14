import json
from helpers.config import Config
import random

class MimicBrain:
    def __init__(self):
        self.brain = self.get_brain()
        self.recent_memory = []
        self.favorite_word = ""
    
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
        
        text_len = len(text.split())
        if text_len == 1:
            self.brain['words'].append(text)
            brain = self.brain
        if text_len > 1 and text_len < 15:
            self.brain['phrase'].append(text)
            brain = self.loop_new_words(text)
            
        elif text_len > 15 and text_len < 20:
            self.brain['sentence'].append(text)
            brain = self.loop_new_words(text)
            
        else:
            brain = self.loop_new_words(text)
        self.save_to_brain(brain)
    
    def loop_new_words(self, text:str):
        for word in text.split():
                self.brain['words'].append(word)
        return self.brain
    
    def save_to_brain(self, data:dict):
        with open(Config.brain_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.brain = self.get_brain()
            
    def find_favorite_word(self)->tuple[bool, str]:
        """
        Returns:
            tuple[bool, str]: Checks if a word was added, string is the word that was added to favorites
        """
        chance = random.randint(1, 100)
        if len(self.brain['favorite_words']) > 3 and chance == 67:

            if self.brain.get('words'): 
                word = random.choice(self.brain['words'])
                self.favorite_word = word
                if word not in self.brain['favorite_words']:
                    self.brain['favorite_words'].append(word)
                
                # Only save when changes are actually made
                self.save_to_brain(self.brain)
            return True, word
        else:
            if 1 / 171547 == 67: # chances of having a favorite word
                if self.brain.get('words'): 
                    word = random.choice(self.brain['words'])
                    self.favorite_word = word
                    if word not in self.brain['favorite_words']:
                        self.brain['favorite_words'].append(word)
                    
                    # Only save when changes are actually made
                    self.save_to_brain(self.brain)
                    return True, word
            
        return False, ""
            
        