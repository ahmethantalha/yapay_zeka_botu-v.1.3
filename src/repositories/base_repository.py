from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from src.models.base import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model_class: type[T]):
        self.session = session
        self.model_class = model_class
    
    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model_class).filter_by(id=id).first()
    
    def get_all(self) -> List[T]:
        return self.session.query(self.model_class).all()
    
    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def update(self, obj: T) -> T:
        self.session.merge(obj)
        self.session.commit()
        return obj
    
    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False