from typing import BinaryIO, Text, List
import logging
from .base_processor import BaseFileProcessor

class TextProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        """Extract text from file"""
        try:
            content = file.read()
            return content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                # Try alternative encodings
                file.seek(0)
                return content.decode('latin-1')
            except Exception as e:
                raise ValueError(f"Failed to decode text file: {str(e)}")

    def get_metadata(self, file: BinaryIO) -> dict:
        """Get text file metadata"""
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset position
        return {
            'size_bytes': size,
            'encoding': 'utf-8'
        }

    def _do_split_file(self, file_path: str, chunk_size: int, method: str) -> List[str]:
        """Split text file into chunks"""
        try:
            self._validate_chunk_size(chunk_size)
            chunks = []
            current_chunk = ""
            
            with open(file_path, 'r', encoding='utf-8') as file:
                if method == "page":
                    chars_per_page = 3000  # Approximate chars per page
                    current_chars = 0
                    
                    for line in file:
                        current_chunk += line
                        current_chars += len(line)
                        
                        if current_chars >= chars_per_page * chunk_size:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                            current_chars = 0
                
                else:  # token based
                    for line in file:
                        current_chunk += line
                        
                        if self.estimate_tokens(current_chunk) >= chunk_size:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
            
            # Add remaining content if any
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            return chunks

        except Exception as e:
            logging.error(f"Error splitting text file {file_path}: {str(e)}")
            raise