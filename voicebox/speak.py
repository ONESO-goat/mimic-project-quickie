import pyttsx3

class Voice:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        
        self.rate = self.engine.getProperty('rate') 
        
        self.volume = self.engine.getProperty("volume")
        
        
        self.voices = self.engine.getProperty('voices') 
        
        if any(x is None for x in [self.rate, self.volume, self.voices]):
            raise ValueError(f"""A text to speech config recieved None: 
                             \nVolume exist: {self.volume is not None}
                             \nVoices exist: {self.voices is not None}
                             \nRate exist: {self.rate is not None}
                             """)
            
        self.engine.setProperty('voice', self.voices[0].id)
        self.engine.setProperty('volume', 0.7)
        self.engine.setProperty('rate', 150)
        
    def change_voice(self, gender_or_option:str):
        import random
        voices = {
            "male": 0,
            "female": 1,
            "random": random.randint(0, 1),
            "other": 1
        }
        gender_or_option = gender_or_option.lower().strip()
        if not gender_or_option or gender_or_option not in voices.keys():
            raise ValueError(f"Paramter is invalid")
        
        self.engine.setProperty("voices", self.voices[voices[gender_or_option]].id)
        
    def change_rate(self, new_rate:int):
        if 200 < new_rate or new_rate < 0:
            raise ValueError(f"{new_rate} is outside the valid range of 1-200")
        
        self.engine.setProperty("rate", new_rate)
        
    def change_volume(self, new_volume:float|int):
        if new_volume > 10:
            raise ValueError(f"{new_volume} is outside the valid range of 0-1")
        if new_volume > 0:
            new_volume = new_volume / 10
        self.engine.setProperty("volume", new_volume)
    
    def say(self, text:str):
        if not text:
            return
        
        self.engine.say(text)
        self.engine.runAndWait()
        
        
    