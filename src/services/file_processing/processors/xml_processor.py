from typing import BinaryIO, Text, List
import xml.etree.ElementTree as ET
from .base_processor import BaseFileProcessor

class XMLProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            content = file.read()
            root = ET.fromstring(content)
            
            # Tüm metin içeriğini almak için recursive işlev
            def get_element_texts(element, indent=0):
                result = ""
                # Element adını ve niteliklerini ekle
                if indent > 0:  # Kök elementi dahil etme
                    result += " " * indent + f"Element: {element.tag}\n"
                    if element.attrib:
                        result += " " * (indent + 2) + f"Nitelikler: {element.attrib}\n"
                
                # Element metnini ekle
                if element.text and element.text.strip():
                    result += " " * (indent + 2) + f"Metin: {element.text.strip()}\n"
                
                # Alt elementleri işle
                for child in element:
                    result += get_element_texts(child, indent + 4)
                
                return result
            
            return get_element_texts(root)
        except Exception as e:
            raise ValueError(f"XML işleme hatası: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        file.seek(0)
        content = file.read()
        root = ET.fromstring(content)
        
        # Element sayılarını hesapla
        element_counts = {}
        for elem in root.iter():
            tag = elem.tag
            element_counts[tag] = element_counts.get(tag, 0) + 1
        
        return {
            'root_element': root.tag,
            'element_counts': element_counts,
            'total_elements': sum(element_counts.values())
        }
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split XML file into chunks
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            if method == "token":
                # XML yapısını bozmadan çocuk elementleri gruplayarak bölme
                chunks = []
                current_chunk = ""
                
                # Her bir ana çocuk elementi için
                for child in root:
                    # Çocuğu XML string'e dönüştür
                    child_str = ET.tostring(child, encoding='unicode')
                    
                    # Eğer mevcut chunk yeterince doluysa, yeni chunk başlat
                    if self.estimate_tokens(current_chunk + child_str) > chunk_size and current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = child_str
                    else:
                        current_chunk += child_str
                
                # Son chunk'ı ekle
                if current_chunk:
                    chunks.append(current_chunk)
                
                # Eğer hiç chunk oluşturamadıysak, tüm XML'i tek parça olarak döndür
                if not chunks:
                    return [ET.tostring(root, encoding='unicode')]
                
                return chunks
            else:
                # Sayfa bazlı bölme için, tüm XML'i tek parça olarak döndür
                return [ET.tostring(root, encoding='unicode')]
        except Exception as e:
            raise ValueError(f"XML dosyası bölünürken hata: {str(e)}")