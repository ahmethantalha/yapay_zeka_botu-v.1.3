from typing import List, Optional
from .base_repository import BaseRepository
from src.models.custom_analysis_type import CustomAnalysisType

class CustomAnalysisRepository(BaseRepository[CustomAnalysisType]):
    """Repository for managing custom analysis types"""
    
    def get_by_name(self, name: str) -> Optional[CustomAnalysisType]:
        """Get custom analysis type by name"""
        return self.session.query(CustomAnalysisType)\
            .filter(CustomAnalysisType.name == name)\
            .first()
    
    def get_all_names(self) -> List[str]:
        """Get all custom analysis type names"""
        try:
            result = self.session.query(CustomAnalysisType.name)\
                .order_by(CustomAnalysisType.name)\
                .all()
            print(f"Repository'den gelen sonuçlar: {result}")  # Debug için
            return [r[0] for r in result]
        except Exception as e:
            print(f"get_all_names'de hata: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def create_custom_type(self, name: str, description: str, prompt_template: str) -> CustomAnalysisType:
        """Create a new custom analysis type"""
        custom_type = CustomAnalysisType(
            name=name,
            description=description,
            prompt_template=prompt_template
        )
        return self.create(custom_type)
    
    def update_custom_type(self, name: str, description: str, prompt_template: str) -> Optional[CustomAnalysisType]:
        """Update existing custom analysis type"""
        custom_type = self.get_by_name(name)
        if custom_type:
            custom_type.description = description
            custom_type.prompt_template = prompt_template
            return self.update(custom_type)
        return None
    
    def delete_by_name(self, name: str) -> bool:
        """Delete custom analysis type by name"""
        custom_type = self.get_by_name(name)
        if custom_type:
            return self.delete(custom_type.id)
        return False