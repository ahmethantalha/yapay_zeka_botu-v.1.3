from typing import List, Optional, Dict, Any
import json
from .base_repository import BaseRepository
from src.models.ai_config import AIConfig

class AIConfigRepository(BaseRepository[AIConfig]):
    def get_active_configs(self) -> List[AIConfig]:
        return self.session.query(AIConfig)\
            .filter_by(is_active=True)\
            .all()
    
    def get_by_provider(self, provider: str) -> Optional[AIConfig]:
        return self.session.query(AIConfig)\
            .filter_by(provider=provider)\
            .first()
    
    def update_config(self, provider: str, settings: Dict[str, Any]) -> AIConfig:
        config = self.get_by_provider(provider)
        if not config:
            config = AIConfig(provider=provider)
        
        config.settings = json.dumps(settings)
        return self.update(config)