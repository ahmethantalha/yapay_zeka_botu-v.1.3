# src/services/file_processing/processors/base_processor.py

from abc import ABC, abstractmethod
from typing import BinaryIO, Text, List

class BaseFileProcessor(ABC):
    @abstractmethod
    def extract_text(self, file: BinaryIO) -> Text:
        """Extract text from file"""
        pass
    
    @abstractmethod
    def get_metadata(self, file: BinaryIO) -> dict:
        """Get file metadata"""
        pass
    
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """Split file into chunks - DEFAULT IMPLEMENTATION"""
        try:
            # Just extract text and return it as a single chunk
            with open(file_path, 'rb') as file:
                extracted_text = self.extract_text(file)
                return [extracted_text]
        except Exception as e:
            print(f"File splitting error in default implementation: {str(e)}")
            return ["Error extracting text: " + str(e)]

    def estimate_tokens(self, text: str) -> int:
        """Estimate number of tokens in text (rough estimation)"""
        # Basit bir tahmin: ortalama 4 karaktere 1 token
        return len(text) // 4