from typing import BinaryIO, Text, List
import pytesseract
from PIL import Image
from io import BytesIO
import os
from .base_processor import BaseFileProcessor

class ImageProcessor(BaseFileProcessor):
    def __init__(self):
        # Tesseract yolunu ayarla - Windows için gerekli
        if os.name == 'nt':  # Windows işletim sistemi kontrolü
            tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            else:
                # Alternatif yolları dene
                alt_path = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
                if os.path.exists(alt_path):
                    pytesseract.pytesseract.tesseract_cmd = alt_path
                else:
                    print("UYARI: Tesseract yolu bulunamadı. Lütfen tesseract-ocr kurulumunu yapın.")
    
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            image = Image.open(file)
            
            # Tesseract'ı kontrol et
            try:
                result = pytesseract.image_to_string(image, lang='tur+eng')
                if not result.strip():
                    # Boş sonuç döndüyse basit bir uyarı mesajı
                    return "[Görüntüden metin çıkarılamadı. Görüntü metin içermiyor olabilir veya Tesseract OCR kurulumu gerekiyor olabilir.]"
                return result
            except Exception as e:
                # Tesseract hatası
                error_msg = str(e)
                if "tesseract is not installed" in error_msg.lower() or "tesseract not found" in error_msg.lower():
                    return "[Tesseract OCR kurulu değil. Görüntü dosyalarını analiz etmek için Tesseract OCR'ı kurmanız gerekmektedir.]"
                else:
                    return f"[Görüntü işleme hatası: {error_msg}]"
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        image = Image.open(file)
        return {
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode
        }
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split image file into chunks - Görüntü dosyaları parçalanamaz, o yüzden tek parça olarak döndürüyoruz
        """
        try:
            # Görüntü dosyaları parçalanamaz, tam görüntüyü işlemek için metni döndürür
            with open(file_path, 'rb') as file:
                extracted_text = self.extract_text(file)
                return [extracted_text]  # Tek bir parça olarak döndür
        except Exception as e:
            raise ValueError(f"Görüntü dosyası bölünürken hata: {str(e)}")