import ollama
from helpers.config import Config
from helpers.prompts import Prompts
from google import genai
            
class Helpers:
    def __init__(self, ai_to_use:str, api_key:str|None=Config.gemini_api) -> None:
  
        if self.backend == 'gemini' and api_key:
            # Use Gemini
            
            
            self.client = genai.Client(api_key=api_key)
            self.llm = 'gemini-2.5-flash'
            
            print(f"✓ Gemini Backend Initialized: {self.client}")
            
        else:
            # Use Ollama
            
            self.backend = 'ollama'
            self.ollama_model = 'qwen3:0.6b'
            
            # Check if Ollama is available
            try:
                import ollama
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")
                
            except:
                print(f"⚠ Ollama model '{self.ollama_model}' not found")
                print("  Run: ollama pull qwen3:0.6b")
    
    def validate_text(self, text:str, threshold):
        prompt = Prompts().validate_text
        m = [
            {"role": "sytstem", "content": prompt},
            {"role": "user", "content": f"<<<TEXT>>>\n{text}\n<<<TEXT>>>"}
        ]
        
        
        
        if backend 