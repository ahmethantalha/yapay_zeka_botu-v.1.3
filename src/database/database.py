from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import AppConfig
from src.models.base import Base

class Database:
    def __init__(self, config: AppConfig):
        self.engine = create_engine(config.db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()