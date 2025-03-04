from typing import BinaryIO, Text, List
from pydub import AudioSegment
import speech_recognition as sr
from io import BytesIO
from .base_processor import BaseFileProcessor

class AudioProcessor(BaseFileProcessor):
    def extract_text(self, file: BinaryIO) -> Text:
        try:
            # Ses dosyasını geçici olarak kaydet
            temp_file = BytesIO(file.read())
            audio = AudioSegment.from_file(temp_file)
            
            # Ses tanıma için kullanılacak recognizer
            recognizer = sr.Recognizer()
            
            # Ses dosyasını WAV formatına dönüştür
            audio.export("temp.wav", format="wav")
            
            # Ses tanıma işlemi
            with sr.AudioFile("temp.wav") as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                
            # Geçici dosyayı temizle
            import os
            if os.path.exists("temp.wav"):
                os.remove("temp.wav")
                
            return text
        except Exception as e:
            raise ValueError(f"Failed to process audio: {str(e)}")
    
    def get_metadata(self, file: BinaryIO) -> dict:
        try:
            file.seek(0)
            temp_file = BytesIO(file.read())
            audio = AudioSegment.from_file(temp_file)
            
            return {
                'channels': audio.channels,
                'sample_width': audio.sample_width,
                'frame_rate': audio.frame_rate,
                'duration_seconds': len(audio) / 1000
            }
        except Exception as e:
            return {
                'error': str(e)
            }
        
    def split_file(self, file_path: str, chunk_size: int, method: str = "token") -> List[str]:
        """
        Split audio file into chunks - Ses dosyaları metin olarak parçalanamaz
        """
        try:
            # Ses dosyasındaki metni çıkar
            with open(file_path, 'rb') as file:
                extracted_text = self.extract_text(file)
                return [extracted_text]  # Tek bir parça olarak döndür
        except Exception as e:
            raise ValueError(f"Ses dosyası bölünürken hata: {str(e)}")