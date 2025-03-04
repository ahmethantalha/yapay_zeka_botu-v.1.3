from typing import BinaryIO, Text, List
import json
from .base_processor import BaseFileProcessor

class JSONProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            json_data = json.load(file)
            return json.dumps(json_data, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Failed to process JSON: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        file.seek(0)
        json_data = json.load(file)
        
        metadata = {
            'keys': list(json_data.keys()) if isinstance(json_data, dict) else [],
            'type': type(json_data).__name__
        }
        
        return metadata
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split JSON file into chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_content = json.load(file)
                
                # JSON'ı metin olarak işle
                json_text = json.dumps(json_content, indent=2, ensure_ascii=False)
                
                if method == "token":
                    # Uzun JSON'ı bölme işlemi
                    chunks = []
                    current_chunk = ""
                    lines = json_text.split('\n')
                    
                    for line in lines:
                        current_chunk += line + '\n'
                        
                        if self.estimate_tokens(current_chunk) >= chunk_size:
                            chunks.append(current_chunk)
                            current_chunk = ""
                    
                    # Kalan kısmı ekle
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    return chunks if chunks else [json_text]
                else:
                    # Sayfa bazlı bölme - JSON için pek anlamlı değil, 
                    # bu yüzden bütün içeriği döndür
                    return [json_text]
        except Exception as e:
            raise ValueError(f"JSON dosyası bölünürken hata: {str(e)}")