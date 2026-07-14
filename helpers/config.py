import os
import dotenv



class Config:
    brain_file = "brain/mimic.json"
    
    # Ollama config
    ollama_model_qwen = ""
    
    # Gemini config
    gemini_model = ""
    gemini_api = 
    
    # AI constraints
    
    
    
    
    
    # functions 
    def change_gemini_api(self, num:int):
        key = os.getenv(f"GEMINI_API_KEY{num}")
        if not key:
            raise ValueError(f"There is no {num} gemini key")

        self.gemini_api = key