import PyPDF2
from typing import BinaryIO, Text, List
import logging
from .base_processor import BaseFileProcessor

class PDFProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        """Extract text from PDF file"""
        try:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    def get_metadata(self, file: BinaryIO) -> dict:
        """Get PDF metadata"""
        try:
            reader = PyPDF2.PdfReader(file)
            info = reader.metadata
            return {
                'page_count': len(reader.pages),
                'author': info.get('/Author', 'Unknown'),
                'title': info.get('/Title', 'Untitled'),
                'subject': info.get('/Subject', ''),
                'creator': info.get('/Creator', '')
            }
        except Exception as e:
            logging.error(f"Error getting PDF metadata: {str(e)}")
            return {'page_count': 0}

    def _do_split_file(self, file_path: str, chunk_size: int, method: str) -> List[str]:
        """Split PDF file into chunks"""
        try:
            self._validate_chunk_size(chunk_size, max_size=100)  # Limit max pages
            chunks = []
            
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                if method == "page":
                    # Split by page count
                    for start in range(0, total_pages, chunk_size):
                        chunk_text = ""
                        end = min(start + chunk_size, total_pages)
                        
                        for page_num in range(start, end):
                            try:
                                page = reader.pages[page_num]
                                text = page.extract_text()
                                if text:
                                    chunk_text += text + "\n\n"
                            except Exception as e:
                                logging.warning(f"Error extracting page {page_num}: {str(e)}")
                                continue
                        
                        if chunk_text.strip():
                            chunks.append(chunk_text.strip())
                
                else:  # token based
                    current_chunk = ""
                    for page in reader.pages:
                        try:
                            text = page.extract_text()
                            if text:
                                current_chunk += text + "\n\n"
                                
                                if self.estimate_tokens(current_chunk) >= chunk_size:
                                    chunks.append(current_chunk.strip())
                                    current_chunk = ""
                        except Exception as e:
                            logging.warning(f"Error processing page: {str(e)}")
                            continue
                    
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
            
            return chunks

        except Exception as e:
            logging.error(f"Error splitting PDF file {file_path}: {str(e)}")
            raise