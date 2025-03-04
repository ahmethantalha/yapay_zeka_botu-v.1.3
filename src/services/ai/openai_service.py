import openai
from .base_ai_service import BaseAIService

class OpenAIService(BaseAIService):
    """OpenAI service implementation"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.Client(api_key=api_key)
        self.model = model
    
    async def analyze_text(self, text: str, prompt_template: str) -> str:
        try:
            print(f"OpenAI API çağrısı başlatılıyor: {self.model}")
            # OpenAI kütüphanesi zaten async/await desteği sağlıyor
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": text}
                ],
                timeout=60  # 60 saniye zaman aşımı (eğer bu parametre destekleniyorsa)
            )
            print("OpenAI API yanıt verdi")
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API hatası: {str(e)}")
            raise ValueError(f"OpenAI API error: {str(e)}")
    
    async def generate_questions(self, text: str, count: int = 5) -> list[str]:
        prompt = f"Generate {count} relevant questions based on the following text:\n\n{text}"
        response = await self.analyze_text(text, prompt)
        return response.split('\n')[:count]