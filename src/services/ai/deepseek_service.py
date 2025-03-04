import aiohttp
import json
from .base_ai_service import BaseAIService

class DeepSeekService(BaseAIService):
    """DeepSeek service implementation"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = model
    
    async def analyze_text(self, text: str, prompt_template: str) -> str:
        try:
            print(f"DeepSeek API çağrısı başlatılıyor: {self.model}")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    headers=headers, 
                    json=data,
                    timeout=60  # 60 saniye zaman aşımı
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    print("DeepSeek API yanıt verdi")
                    return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"DeepSeek API hatası: {str(e)}")
            raise ValueError(f"DeepSeek API error: {str(e)}")
    
    async def generate_questions(self, text: str, count: int = 5) -> list[str]:
        prompt = f"Generate {count} relevant questions based on the following text."
        response = await self.analyze_text(text, prompt)
        lines = response.split('\n')
        questions = [line for line in lines if line.strip() and ('?' in line)]
        return questions[:count]