from faster_whisper import WhisperModel
import random
import speech_recognition as sr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CyberLife.BrainAnomaly.BrainAnomaly import Brain

class Ears:
    def __init__(self, engine=None, use_whisper:bool=False):
        self.wav_file_path = "voicebox/audio/user_audio.wav"
        self.whisper_model = None
        if use_whisper:
            self.whisper_model = WhisperModel(self.wav_file_path)

        self.recognizer = sr.Recognizer()
        assert self.recognizer is not None, "Reconizer wasn't configured"
    
    def wait_for_wake_word(self, wake_word: str = "mimic") -> bool|str:
        """
        Loops indefinitely, listening for a short snippet of audio.
        Returns True when the wake word is detected, returns 'random' for the mimic to say something random
        """
        print(f"Passive listening... Say '{wake_word}' to activate.")
        
        while True:
            num = random.randint(1,25)
            if num == 10:
                return "random"
            
            with sr.Microphone() as source:
                
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:

                    audio_stream = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                    

                    text_result = self.recognizer.recognize_google(audio_stream).lower()
                    
                    if wake_word in text_result:
                        print(f" Wake word '{wake_word}' detected!")
                        return True
                        
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"API service error in passive loop: {e}")
                    continue
        
    def sr_listen(self, silence_timeout:float=1.5, energy_threshold:int=400):  

        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please stay quiet.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.recognizer.pause_threshold = silence_timeout
            self.recognizer.energy_threshold = energy_threshold 
        
        
            print("Listening... Speak now.")
            
            # Capture the live audio stream
            audio_stream = self.recognizer.listen(source, timeout=10)

        try:
            print("Transcribing your audio...")
            # Process speech using Google's free web API
            text_result = self.recognizer.recognize_google(audio_stream)
            print(f"Heard: {text_result}")
            return text_result
        
        except sr.WaitTimeoutError:
            print("Error: You didn't start speaking within 10 seconds.")
            return ""
        
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return ""
        
        except sr.RequestError as e:
            print(f"API service error: {e}")
            return ""
            
    def wav_breakdown(self, path="audio/audio.wav"):
        try:
            segments, info = self.whisper_model.transcribe(path)

            text = " ".join([s.text for s in segments]).strip()
            
            return text

        except Exception as e:
            print("Whisper error:", e)
            return ""
        
        
    