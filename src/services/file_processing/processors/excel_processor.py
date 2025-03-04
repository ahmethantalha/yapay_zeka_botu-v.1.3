from typing import BinaryIO, Text
import pandas as pd
from .base_processor import BaseFileProcessor

class ExcelProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            df = pd.read_excel(file)
            return df.to_string()
        except Exception as e:
            raise ValueError(f"Failed to process Excel: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names
        
        metadata = {
            'sheets': sheet_names,
            'sheet_count': len(sheet_names)
        }
        
        return metadata