import os
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class AppConfig:
    """Application configuration class"""
    
    def __init__(self):
        self.api_keys: Dict[str, str] = {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'gemini': os.getenv('GEMINI_API_KEY', ''),
            'anthropic': os.getenv('ANTHROPIC_API_KEY', '')
        }
        
        self.db_url: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        self.temp_dir: str = os.getenv('TEMP_DIR', 'temp')
        self.max_file_size: int = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB default
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)