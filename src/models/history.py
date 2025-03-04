from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary
from datetime import datetime
import pickle
from .base import Base

class AnalysisHistory(Base):
    __tablename__ = 'analysis_history'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    analysis_type = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)  # Kısa özet - ilk birkaç satır
    result_data = Column(LargeBinary)  # Tam sonuç - pickle ile kaydedilecek
    
    @property
    def formatted_date(self):
        """Return formatted date string"""
        return self.timestamp.strftime('%d.%m.%Y %H:%M')