from sqlalchemy import Column, Integer, String, Boolean, Float
from .base import Base

class AIConfig(Base):
    __tablename__ = 'ai_configs'
    
    id = Column(Integer, primary_key=True)
    provider = Column(String(50), nullable=False)  # openai, gemini, anthropic
    is_active = Column(Boolean, default=True)
    model_name = Column(String(50))
    max_tokens = Column(Integer, default=2000)
    temperature = Column(Float, default=0.7)
    settings = Column(String(1024))  # JSON string for additional settings