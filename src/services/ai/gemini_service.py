import google.generativeai as genai
from .base_ai_service import BaseAIService
import asyncio

class GeminiService(BaseAIService):
    """Google Gemini service implementation"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)
    
    async def analyze_text(self, text: str, prompt_template: str) -> str:
        try:
            print(f"Gemini API çağrısı başlatılıyor: {self.model_name}")
            loop = asyncio.get_event_loop()
            
            # Senkron çağrıyı asenkron bir şekilde çalıştır
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(f"{prompt_template}\n\nText to analyze: {text}")
            )
            print("Gemini API yanıt verdi")
            return response.text
        except Exception as e:
            print(f"Gemini API hatası: {str(e)}")
            raise ValueError(f"Gemini API error: {str(e)}")
    
    async def generate_questions(self, text: str, count: int = 5) -> list[str]:
        prompt = f"Generate {count} relevant questions based on the following text:\n\n{text}"
        response = await self.analyze_text(text, prompt)
        return response.split('\n')[:count]