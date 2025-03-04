from typing import BinaryIO, Text, List
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from .base_processor import BaseFileProcessor

class EPUBProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            # Geçici dosya oluştur (ebooklib dosya nesnesi değil yol bekliyor)
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as temp:
                temp.write(file.read())
                temp_path = temp.name
            
            # EPUB dosyasını işle
            book = epub.read_epub(temp_path)
            
            # Geçici dosyayı sil
            os.unlink(temp_path)
            
            # İçerik metinlerini topla
            contents = []
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    contents.append(soup.get_text())
            
            return "\n\n".join(contents)
        except Exception as e:
            raise ValueError(f"EPUB işleme hatası: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        try:
            # Geçici dosya oluştur
            import tempfile
            import os
            
            file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as temp:
                temp.write(file.read())
                temp_path = temp.name
            
            # EPUB dosyasını işle
            book = epub.read_epub(temp_path)
            
            # Geçici dosyayı sil
            os.unlink(temp_path)
            
            # Metadata
            metadata = {
                'title': book.get_metadata('DC', 'title'),
                'creator': book.get_metadata('DC', 'creator'),
                'language': book.get_metadata('DC', 'language'),
                'identifier': book.get_metadata('DC', 'identifier'),
                'document_count': len([item for item in book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT])
            }
            
            return metadata
        except Exception as e:
            raise ValueError(f"EPUB metadata hatası: {str(e)}")
            
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split EPUB file into chunks
        """
        try:
            import os
            # EPUB dosyasını işle
            book = epub.read_epub(file_path)
            
            # Bölümlere ayır
            chapters = []
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    chapter_text = soup.get_text()
                    if chapter_text.strip():
                        chapters.append(chapter_text)
            
            if method == "token":
                # Her bölümü token limitine göre parçala
                chunks = []
                current_chunk = ""
                
                for chapter in chapters:
                    lines = chapter.split('\n')
                    
                    for line in lines:
                        if not line.strip():
                            continue
                            
                        if self.estimate_tokens(current_chunk + line) > chunk_size and current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = line + "\n"
                        else:
                            current_chunk += line + "\n"
                
                # Son chunk'ı ekle
                if current_chunk:
                    chunks.append(current_chunk)
                
                return chunks if chunks else ["".join(chapters)]
            else:
                # Sayfa bazlı bölme - her bölümü ayrı bir sayfa olarak düşün
                return chapters if chapters else ["".join(chapters)]
                
        except Exception as e:
            raise ValueError(f"EPUB dosyası bölünürken hata: {str(e)}")