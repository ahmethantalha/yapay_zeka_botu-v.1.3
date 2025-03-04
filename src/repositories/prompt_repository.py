from typing import List, Optional
from .base_repository import BaseRepository
from src.models.prompt_template import PromptTemplate

class PromptRepository(BaseRepository[PromptTemplate]):
    def get_by_user(self, user_id: int) -> List[PromptTemplate]:
        return self.session.query(PromptTemplate)\
            .filter_by(user_id=user_id)\
            .all()
    
    def get_by_name(self, user_id: int, name: str) -> Optional[PromptTemplate]:
        return self.session.query(PromptTemplate)\
            .filter_by(user_id=user_id, name=name)\
            .first()