import os
import dotenv


dotenv.load_dotenv("agent_keys")
class Config:
    brain_file = "brain/mimic.json"
    
    # Ollama config
    ollama_model_qwen = 'qwen3:0.6b'
    
    # Gemini config
    gemini_model_id = 'gemini-2.5-flash'
    gemini_api = os.getenv("GEMINI_API_KEY1")
    
    # AI constraints
    thresholds =  None
    
    
    
    
    
    # functions 
    def change_gemini_api(self, num:int):
        key = os.getenv(f"GEMINI_API_KEY{num}")
        if not key:
            raise ValueError(f"There is no {num} gemini key")

        self.gemini_api = key