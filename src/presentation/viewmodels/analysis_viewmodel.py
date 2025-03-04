from typing import Optional, List
import asyncio
from src.services.ai_service_manager import AIServiceManager

class AnalysisViewModel:
    def __init__(self, ai_service_manager: AIServiceManager):
        self.ai_service_manager = ai_service_manager
        self.current_provider: str = "openai"
        self.current_text: Optional[str] = None
        
        # Callbacks
        self._on_analysis_complete = None
        self._on_error = None
    
    def set_callbacks(self, on_analysis_complete, on_error):
        self._on_analysis_complete = on_analysis_complete
        self._on_error = on_error
    
    async def analyze_text(self, text: str, analysis_type: str):
        """Analyze text using current AI provider"""
        try:
            self.current_text = text
            
            if analysis_type == "Soru-Cevap":
                questions = await self.ai_service_manager.generate_questions(
                    text,
                    self.current_provider
                )
                result = "Oluşturulan Sorular:\n\n" + "\n".join(questions)
            else:
                # Get prompt template based on analysis type
                prompt = self._get_prompt_for_analysis_type(analysis_type)
                
                result = await self.ai_service_manager.analyze_text(
                    text,
                    self.current_provider,
                    prompt
                )
            
            if self._on_analysis_complete:
                self._on_analysis_complete(result)
                
        except Exception as e:
            if self._on_error:
                self._on_error(str(e))
    
    def change_provider(self, provider: str):
        """Change current AI provider"""
        self.current_provider = provider
    
    def _get_prompt_for_analysis_type(self, analysis_type: str) -> str:
        """Get prompt template for analysis type"""
        # Delegate to main view model for consistency
        from .main_viewmodel import MainViewModel
        dummy_viewmodel = MainViewModel(None)  # Just to access the method
        return dummy_viewmodel._get_prompt_for_analysis_type(analysis_type)