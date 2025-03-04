import anthropic
from .base_ai_service import BaseAIService
import asyncio

class ClaudeService(BaseAIService):
    """Anthropic Claude service implementation"""
    
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    async def analyze_text(self, text: str, prompt_template: str) -> str:
        try:
            print(f"Claude API çağrısı başlatılıyor: {self.model}")
            loop = asyncio.get_event_loop()
            
            # Senkron çağrıyı asenkron bir şekilde çalıştır
            message = await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.7,
                    system=prompt_template,
                    messages=[
                        {"role": "user", "content": text}
                    ]
                )
            )
            print("Claude API yanıt verdi")
            return message.content[0].text
        except Exception as e:
            print(f"Claude API hatası: {str(e)}")
            raise ValueError(f"Claude API error: {str(e)}")
    
    async def generate_questions(self, text: str, count: int = 5) -> list[str]:
        prompt = f"Generate {count} relevant questions based on the following text."
        response = await self.analyze_text(text, prompt)
        # Claude'un yanıtını satır bazında bölerek soruları alıyoruz
        lines = response.split('\n')
        questions = [line for line in lines if line.strip() and ('?' in line)]
        return questions[:count]