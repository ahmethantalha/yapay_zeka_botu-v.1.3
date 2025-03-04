from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAIService(ABC):
    """Base class for AI services"""
    
    @abstractmethod
    async def analyze_text(self, text: str, prompt_template: str) -> str:
        """
        Analyze text using the AI model with the provided prompt template.
        
        Args:
            text (str): The text to analyze
            prompt_template (str): The template to structure the prompt
            
        Returns:
            str: The analyzed result from the AI model
        """
        pass
    
    @abstractmethod
    async def generate_questions(self, text: str, count: int = 5) -> List[str]:
        """
        Generate questions based on the text.
        
        Args:
            text (str): The text to generate questions from
            count (int): Number of questions to generate
            
        Returns:
            List[str]: List of generated questions
        """
        pass
    
    def get_model_name(self) -> str:
        """
        Get the name of the AI model being used.
        
        Returns:
            str: The model name
        """
        if hasattr(self, 'model'):
            return str(self.model)
        return "unknown"
    
    def get_service_name(self) -> str:
        """
        Get the name of the AI service.
        
        Returns:
            str: The service name derived from the class name
        """
        class_name = self.__class__.__name__
        if class_name.endswith('Service'):
            return class_name[:-7].lower()
        return class_name.lower()
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this AI service.
        
        Returns:
            Dict[str, Any]: Dictionary of capabilities
        """
        return {
            "text_analysis": True,
            "question_generation": True,
            "model": self.get_model_name(),
            "service": self.get_service_name()
        }