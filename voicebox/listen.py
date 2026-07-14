from faster_whisper import WhisperModel
import ollama
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CyberLife.BrainAnomaly.BrainAnomaly import Brain

class Ears:
    def __init__(self, brain: "Brain", agent_to_use:str, model:str):
        self.wav_file_path = "audio/user_audio.wav"
        self.ai = agent_to_use
        self.whisper_model = WhisperModel(self.wav_file_path)
        self.brain = brain
        self.memories = self.brain.get_storage()
        

    def wav_breakdown(self, path="audio/audio.wav"):
        try:
            segments, info = self.whisper_model.transcribe(path)

            text = " ".join([s.text for s in segments]).strip()
            
            return text

        except Exception as e:
            print("Whisper error:", e)
            return ""
        
        
    