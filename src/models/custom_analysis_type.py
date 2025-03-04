from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .base import Base

class CustomAnalysisType(Base):
    __tablename__ = 'custom_analysis_types'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    prompt_template = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)