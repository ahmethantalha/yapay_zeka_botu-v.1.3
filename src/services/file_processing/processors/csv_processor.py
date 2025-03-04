from typing import BinaryIO, Text, List
import pandas as pd
import io
from .base_processor import BaseFileProcessor

class CSVProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            content = file.read()
            file_like = io.BytesIO(content)
            df = pd.read_csv(file_like)
            
            # Veriyi okunabilir bir metne dönüştür
            text = f"CSV dosyası içeriği:\n\n"
            text += f"Sütunlar: {', '.join(df.columns)}\n\n"
            text += f"Satır sayısı: {len(df)}\n\n"
            text += f"Örnek veriler (ilk 5 satır):\n{df.head().to_string()}\n\n"
            text += f"İstatistikler:\n{df.describe().to_string()}"
            
            return text
        except Exception as e:
            raise ValueError(f"CSV işleme hatası: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        file.seek(0)
        content = file.read()
        file_like = io.BytesIO(content)
        df = pd.read_csv(file_like)
        
        return {
            'columns': list(df.columns),
            'rows': len(df),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split CSV file into chunks
        """
        try:
            df = pd.read_csv(file_path)
            
            if method == "page":
                # "Sayfa" kavramını satır sayısı olarak düşünüyoruz
                rows_per_chunk = chunk_size * 50  # Örnek olarak bir sayfada 50 satır kabul edelim
                
                chunks = []
                for i in range(0, len(df), rows_per_chunk):
                    end_idx = min(i + rows_per_chunk, len(df))
                    chunk_df = df.iloc[i:end_idx]
                    chunk_text = f"CSV kesiti (satır {i+1}-{end_idx}):\n\n"
                    chunk_text += chunk_df.to_string()
                    chunks.append(chunk_text)
                
                return chunks if chunks else [df.to_string()]
            else:
                # Token-based splitting - tüm içeriği bir metin olarak alıp token'lara böleriz
                csv_text = df.to_string()
                
                chunks = []
                current_chunk = ""
                lines = csv_text.split('\n')
                
                for line in lines:
                    current_chunk += line + '\n'
                    
                    if self.estimate_tokens(current_chunk) >= chunk_size:
                        chunks.append(current_chunk)
                        current_chunk = ""
                
                if current_chunk:
                    chunks.append(current_chunk)
                
                return chunks if chunks else [csv_text]
        except Exception as e:
            raise ValueError(f"CSV dosyası bölünürken hata: {str(e)}")