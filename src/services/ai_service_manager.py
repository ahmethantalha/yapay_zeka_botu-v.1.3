import os
import json
from typing import Dict, Any
from .ai.base_ai_service import BaseAIService
from .ai.openai_service import OpenAIService
from .ai.gemini_service import GeminiService
from .ai.claude_service import ClaudeService
from .ai.deepseek_service import DeepSeekService
from src.repositories.ai_config_repository import AIConfigRepository
from src.core.security import Security

class AIServiceManager:
    def __init__(self, ai_config_repo: AIConfigRepository, security: Security):
        self.ai_config_repo = ai_config_repo
        self.security = security
        self.services: Dict[str, BaseAIService] = {}
        
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize AI services from configuration"""
        try:
            settings = self._load_settings()
            
            # OpenAI
            openai_api_key = os.getenv('OPENAI_API_KEY')
            openai_model = settings.get("openai", {}).get("model", "gpt-3.5-turbo")
            if openai_api_key:
                print(f"OpenAI servisini başlatma: {openai_model}")
                self.services['openai'] = OpenAIService(openai_api_key, openai_model)
            
            # Gemini
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            gemini_model = settings.get("gemini", {}).get("model", "gemini-2.0-flash")
            if gemini_api_key:
                print(f"Gemini servisini başlatma: {gemini_model}")
                self.services['gemini'] = GeminiService(gemini_api_key, gemini_model)
            
            # Claude
            claude_api_key = os.getenv('CLAUDE_API_KEY')
            claude_model = settings.get("claude", {}).get("model", "claude-3-opus-20240229")
            if claude_api_key:
                print(f"Claude servisini başlatma: {claude_model}")
                self.services['claude'] = ClaudeService(claude_api_key, claude_model)
            
            # DeepSeek
            deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
            deepseek_model = settings.get("deepseek", {}).get("model", "deepseek-chat")
            if deepseek_api_key:
                print(f"DeepSeek servisini başlatma: {deepseek_model}")
                self.services['deepseek'] = DeepSeekService(deepseek_api_key, deepseek_model)
            
            # Default AI provider
            self.default_provider = settings.get("default_ai", "OpenAI").lower()
            if self.default_provider not in self.services and self.services:
                self.default_provider = list(self.services.keys())[0]
                
            # Log active services
            print(f"Aktif AI servisleri: {', '.join(self.services.keys()) if self.services else 'Yok'}")
            
        except Exception as e:
            print(f"AI servisleri başlatılırken hata oluştu: {str(e)}")
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        try:
            settings_file = os.path.join(os.path.dirname(__file__), "../../data/settings.json")
            
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ayarlar yüklenirken hata: {str(e)}")
        
        return {}
    
    async def analyze_text(self, text: str, provider: str, prompt_template: str) -> str:
        """Analyze text using specified AI service"""
        print(f"analyze_text çağrıldı: provider={provider}, metin uzunluğu={len(text)}")
        
        try:
            # Eğer belirtilen sağlayıcı yoksa, mevcut bir servis kullan
            if provider not in self.services:
                print(f"Belirtilen provider '{provider}' mevcut değil")
                if self.default_provider in self.services:
                    print(f"Varsayılan provider kullanılıyor: {self.default_provider}")
                    provider = self.default_provider
                elif len(self.services) > 0:
                    provider = list(self.services.keys())[0]
                    print(f"İlk bulunan provider kullanılıyor: {provider}")
                else:
                    raise ValueError("Hiçbir AI servisi yapılandırılmamış. API anahtarlarınızı kontrol edin.")
            
            print(f"Kullanılan provider: {provider}")
            service = self.services[provider]
            print(f"Servis bulundu: {type(service).__name__}")
            
            print("AI servisi analiz başlatılıyor...")
            result = await service.analyze_text(text, prompt_template)
            print(f"AI servisi yanıt verdi, yanıt uzunluğu: {len(result)}")
            return result
            
        except Exception as e:
            print(f"AI servisi hatası: {str(e)}")
            raise ValueError(f"AI analiz hatası: {str(e)}")
    
    async def generate_questions(self, text: str, provider: str, count: int = 5) -> list[str]:
        """Generate questions using specified AI service"""
        print(f"generate_questions çağrıldı: provider={provider}, metin uzunluğu={len(text)}")
        
        try:
            # Eğer belirtilen sağlayıcı yoksa, mevcut bir servis kullan
            if provider not in self.services:
                print(f"Belirtilen provider '{provider}' mevcut değil")
                if self.default_provider in self.services:
                    print(f"Varsayılan provider kullanılıyor: {self.default_provider}")
                    provider = self.default_provider
                elif len(self.services) > 0:
                    provider = list(self.services.keys())[0]
                    print(f"İlk bulunan provider kullanılıyor: {provider}")
                else:
                    raise ValueError("Hiçbir AI servisi yapılandırılmamış. API anahtarlarınızı kontrol edin.")
            
            print(f"Kullanılan provider: {provider}")
            service = self.services[provider]
            print(f"Servis bulundu: {type(service).__name__}")
            
            print("AI servisi soru üretimi başlatılıyor...")
            questions = await service.generate_questions(text, count)
            print(f"AI servisi {len(questions)} soru üretti")
            return questions
            
        except Exception as e:
            print(f"AI servisi hatası: {str(e)}")
            raise ValueError(f"Soru üretme hatası: {str(e)}")