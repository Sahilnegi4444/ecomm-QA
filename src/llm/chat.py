import requests
from src.logger import logging

class LLMconfig:
    def __init__(self):
        pass  

class LLMchat:
    def __init__(self, use_ollama = True):
        self.use_ollama = use_ollama

    def generate(self,prompt):
        self.prompt = prompt
        if self.use_ollama:
            return self.generate_ollama(prompt)
        
        else:
            return "No model is initiated"

    def generate_ollama(self, prompt):
        """
        Ollama generation
        """
        try:
            payload = {
                'model': 'llama3.1:8b', 
                'prompt': prompt, 
                'stream': False
            }

            response = requests.post(
                'http://localhost:11434/api/generate',
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            
            
            return response.json()['response']

        except Exception as e:
            raise str(e)

