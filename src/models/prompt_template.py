from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from .base import Base

class PromptTemplate(Base):
    __tablename__ = 'prompt_templates'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    template_text = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)