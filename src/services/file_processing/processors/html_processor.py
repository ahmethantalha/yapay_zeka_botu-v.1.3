from typing import BinaryIO, Text, List
from bs4 import BeautifulSoup
from .base_processor import BaseFileProcessor

class HTMLProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            content = file.read().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Script ve style etiketlerini kaldır
            for script in soup(["script", "style"]):
                script.extract()
            
            # Metin içeriğini al
            text = soup.get_text(separator='\n')
            
            # Gereksiz boşlukları temizle
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            raise ValueError(f"HTML işleme hatası: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        file.seek(0)
        content = file.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        
        # Metatag'leri topla
        meta_tags = {}
        for tag in soup.find_all('meta'):
            if tag.get('name'):
                meta_tags[tag.get('name')] = tag.get('content')
        
        return {
            'title': soup.title.string if soup.title else None,
            'meta_tags': meta_tags,
            'links': len(soup.find_all('a')),
            'images': len(soup.find_all('img')),
            'paragraphs': len(soup.find_all('p'))
        }
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split HTML file into chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Script ve style etiketlerini kaldır
                for script in soup(["script", "style"]):
                    script.extract()
                
                if method == "token":
                    # HTML belgesini paragraf, başlık vb. öğelere göre böl
                    chunks = []
                    current_chunk = ""
                    
                    # Anlamlı bölümler: p, div, h1-h6, article, section, ...
                    elements = soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                                            'article', 'section', 'li', 'blockquote'])
                    
                    for elem in elements:
                        elem_text = elem.get_text(strip=True)
                        if not elem_text:
                            continue
                            
                        if self.estimate_tokens(current_chunk + elem_text) > chunk_size and current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = elem_text + "\n\n"
                        else:
                            current_chunk += elem_text + "\n\n"
                    
                    # Son chunk'ı ekle
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    return chunks if chunks else [soup.get_text()]
                else:
                    # Sayfa bazlı bölme - tek sayfa olarak düşün
                    return [soup.get_text()]
        except Exception as e:
            raise ValueError(f"HTML dosyası bölünürken hata: {str(e)}")