import os
from typing import Dict, Type
from .processors.base_processor import BaseFileProcessor
from .processors.pdf_processor import PDFProcessor
from .processors.docx_processor import DocxProcessor
from .processors.excel_processor import ExcelProcessor
from .processors.image_processor import ImageProcessor
from .processors.text_processor import TextProcessor
from .processors.json_processor import JSONProcessor
from .processors.csv_processor import CSVProcessor  # YENİ!
from .processors.html_processor import HTMLProcessor  # YENİ!
from .processors.xml_processor import XMLProcessor  # YENİ!
from .processors.epub_processor import EPUBProcessor  # YENİ!
from .processors.audio_processor import AudioProcessor  # type: ignore # YENİ!

class FileProcessorFactory:
    def __init__(self):
        self._processors: Dict[str, Type[BaseFileProcessor]] = {
            '.pdf': PDFProcessor,
            '.docx': DocxProcessor,
            '.xlsx': ExcelProcessor,
            '.xls': ExcelProcessor,
            '.png': ImageProcessor,
            '.jpg': ImageProcessor,
            '.jpeg': ImageProcessor,
            '.txt': TextProcessor,
            '.json': JSONProcessor,
            '.csv': CSVProcessor,  # YENİ!
            '.html': HTMLProcessor,  # YENİ!
            '.htm': HTMLProcessor,  # YENİ!
            '.xml': XMLProcessor,  # YENİ!
            '.epub': EPUBProcessor,  # YENİ!
            '.mp3': AudioProcessor,
            '.wav': AudioProcessor,
            '.m4a': AudioProcessor,
            '.flac': AudioProcessor
        }
    
    def get_processor(self, file_path: str) -> BaseFileProcessor:
        """Get appropriate processor for file type"""
        ext = os.path.splitext(file_path)[1].lower()
        processor_class = self._processors.get(ext)
        
        if not processor_class:
            raise ValueError(f"Desteklenmeyen dosya türü: {ext}")
        
        return processor_class()