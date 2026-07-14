import ollama
from helpers.config import Config
from helpers.prompts import Prompts
import json
from typing import Any
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
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")
                
            except:
                print(f"⚠ Ollama model '{self.ollama_model}' not found")
                print("  Run: ollama pull qwen3:0.6b")
                
    def validate_text(self, text:str, threshold=None):
        return self._genrate(text=text, system_prompt=Prompts().validate_text, return_json=True)
    
    def _genrate(self, text:str, system_prompt:str, return_json:bool=False, _use_ollama:bool=False):
        prompt = Prompts().validate_text
        m = [
            {"role": "sytstem", "content": system_prompt},
            {"role": "user", "content": f"<<<TEXT>>>\n{text}\n<<<TEXT>>>"}
        ]
        
        
        
        if self.backend == 'gemini' and not _use_ollama:
            try:
                from google.genai import types
                
                # For Gemini, we convert the messages to their content format
                # Note: Gemini 2.0+ handles system_instruction separately
             
                response = self.client.models.generate_content(
                    model=self.llm, 
                    contents=prompt, # Or pass the whole history
                    config=types.GenerateContentConfig( 
                        #system_instruction=p, # Best way for Gemini
                        response_mime_type="application/json"
                    )
                )
                
                
                return response.text or '[]'
            except Exception as e:
                print(f"[engine.generate gemini] ⚠️ Gemini error: {e}")
                if "503" in str(e):
                    print("⚠️ Gemini service unavailable, switching to ollama, please hold...")
                    self.backend = 'ollama'
                    return self._genrate(text=text, system_prompt=system_prompt, return_json=return_json, _use_ollama=True)  # Retry with Ollama
                return '[]'
        
        else:  # Ollama
            try:

                response = ollama.chat(
                    model=self.ollama_model,
                    messages=m,
                    options={'temperature': 0.2}
                )
                return response['message']['content']
                
            except Exception as e:
                print(f"⚠️ [engine.generate] Ollama error: {e}")
                
                return '[]'
            
    
    def _parse_json(self, text: str, default: Any = None) -> Any:
        """Robust JSON parsing."""
        if not text or text.strip() == '':
            return default if default is not None else []
        
        text = text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Try to parse
        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError as e:
            print(f"⚠ JSON parse error: {e}")
            print(f"  Raw text: {text[:200]}...")
            return default if default is not None else []
        
            