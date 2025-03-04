import asyncio
from typing import Optional, Callable
import customtkinter as ctk
from datetime import datetime
import json
import os
from src.services.file_processing.file_processor_factory import FileProcessorFactory
from src.services.file_processing.result_manager import ProcessingResult, ResultManager
from src.services.ai_service_manager import AIServiceManager
from src.core.prompts import AnalysisPrompts

class MainViewModel:
    def __init__(self, ai_service_manager: AIServiceManager):
        self.file_processor_factory = FileProcessorFactory()
        self.result_manager = ResultManager()
        self.ai_service_manager = ai_service_manager
        self.history_repo = None  # YENİ! HistoryRepository referansı
        
        # State
        self.current_file: Optional[str] = None
        self.current_text: Optional[str] = None
        self.processing_status: str = ""
        self.current_provider: str = "gemini"

        # File processing settings
        self.processing_settings = {
            'auto_split': False,
            'chunk_size': 3,
            'min_split_size': 0.5,  # MB cinsinden
            'combine_method': 'sequential',
            'parallel_processing': False,
            'enable_cache': True
        }

        # Callbacks
        self._on_processing_complete = None
        self._on_status_changed = None
        self._on_progress_start = None  # YENİ!
        self._on_progress_stop = None   # YENİ!
        self._on_error = None
        self._on_settings_saved = None  # YENİ!
        
    def get_setting(self, key: str, default=None):
        """Get file processing setting"""
        return self.processing_settings.get(key, default)

    def get_current_theme(self):
        """Get current theme setting"""
        return "dark"  # varsayılan değer

    def set_theme(self, theme: str):
        """Set and apply theme"""
        ctk.set_appearance_mode(theme)

    def set_callbacks(self, **kwargs):
        """Set callbacks with flexible parameters"""
        if 'on_processing_complete' in kwargs:
            self._on_processing_complete = kwargs['on_processing_complete']
        if 'on_status_changed' in kwargs:
            self._on_status_changed = kwargs['on_status_changed']
        if 'on_progress_start' in kwargs:
            self._on_progress_start = kwargs['on_progress_start']
        if 'on_progress_stop' in kwargs:
            self._on_progress_stop = kwargs['on_progress_stop']
        if 'on_error' in kwargs:
            self._on_error = kwargs['on_error']
        if 'on_settings_saved' in kwargs:
            self._on_settings_saved = kwargs['on_settings_saved']

    

    def get_processing_settings(self) -> dict:
        """Get current processing settings"""
        return self.processing_settings.copy()
    
    def update_processing_settings(self, settings: dict):
        """Update processing settings"""
        self.processing_settings.update(settings)
    
    async def process_file(self, file_path: str, analysis_type: str, progress_callback=None):
        """Process file and perform AI analysis"""
        try:
            # Progress başlat
            if self._on_progress_start:
                self._on_progress_start()
                    
            self._update_status(f"'{os.path.basename(file_path)}' işleniyor...")
            self.current_file = file_path
            
            # İlerleme bildirimi - başlangıç
            if progress_callback:
                progress_callback(0.1, "Dosya işleniyor...")
            
            # Get appropriate processor
            processor = self.file_processor_factory.get_processor(file_path)
            
            # İlerleme bildirimi - processor bulundu
            if progress_callback:
                progress_callback(0.2, f"Dosya türü belirlendi: {os.path.splitext(file_path)[1]}")
            
            # Dosya boyutunu kontrol et
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # MB'a çevir
            
            # İlerleme bildirimi - dosya boyutu
            if progress_callback:
                progress_callback(0.3, f"Dosya boyutu: {file_size_mb:.2f} MB")
            
            # Extract text from file
            with open(file_path, 'rb') as file:
                if progress_callback:
                    progress_callback(0.4, "Metin çıkarılıyor...")
                    
                extracted_text = processor.extract_text(file)
                
                if progress_callback:
                    progress_callback(0.5, f"Metin çıkarıldı: {len(extracted_text)} karakter")
                    
                file.seek(0)
                metadata = processor.get_metadata(file)
            
            # İlerleme bildirimi - AI analizi
            if progress_callback:
                progress_callback(0.7, f"AI analizi başlatılıyor ({self.current_provider})...")
            
            # Get prompt template
            prompt_template = self._get_prompt_for_analysis_type(analysis_type)
            
            # AI analizi
            if progress_callback:
                progress_callback(0.8, "Metin analiz ediliyor...")
                
            analyzed_text = await self.ai_service_manager.analyze_text(
                extracted_text,
                self.current_provider,
                prompt_template
            )
            
            # İlerleme bildirimi - tamamlandı
            if progress_callback:
                progress_callback(0.95, "Analiz tamamlandı, sonuçlar hazırlanıyor...")
            
            result = ProcessingResult(
                original_text=extracted_text,
                analyzed_text=analyzed_text,
                metadata=metadata,
                timestamp=datetime.now(),
                file_name=os.path.basename(file_path),
                analysis_type=analysis_type
            )
            
            # Save to history
            if self.history_repo:
                try:
                    self.history_repo.save_analysis(result, self.current_provider)
                    if progress_callback:
                        progress_callback(0.98, "Analiz geçmişe kaydedildi")
                except Exception as e:
                    print(f"Geçmiş kaydedilirken hata: {str(e)}")
            
            # skip_result_callback parametresine göre callback'i atla
            if not skip_result_callback and self._on_processing_complete:
                self._on_processing_complete(result)
            
            # İlerleme bildirimi - tamamen tamamlandı
            if progress_callback:
                progress_callback(1.0, "İşlem tamamlandı")
                
            return result
            
        except Exception as e:
            self._update_status(f"Hata: {str(e)}")
            if self._on_error:
                self._on_error(str(e))
            return None
            
        finally:
            if self._on_progress_stop:
                self._on_progress_stop()

    async def process_file(self, file_path: str, analysis_type: str, progress_callback=None, skip_result_callback=False):
        """Process file and perform AI analysis"""
        try:
            # Progress başlat
            if self._on_progress_start:
                self._on_progress_start()
                    
            self._update_status(f"'{os.path.basename(file_path)}' işleniyor...")
            self.current_file = file_path
            
            # Get appropriate processor
            processor = self.file_processor_factory.get_processor(file_path)
            
            # İlerleme bildirimi
            if progress_callback:
                progress_callback(0.2, f"Dosya türü belirlendi: {os.path.splitext(file_path)[1]}")
            
            # Normal işleme...
            with open(file_path, 'rb') as file:
                if progress_callback:
                    progress_callback(0.4, "Metin çıkarılıyor...")
                    
                extracted_text = processor.extract_text(file)
                
                if progress_callback:
                    progress_callback(0.5, f"Metin çıkarıldı: {len(extracted_text)} karakter")
                    
                file.seek(0)
                metadata = processor.get_metadata(file)
            
            # İlerleme bildirimi
            if progress_callback:
                progress_callback(0.7, f"AI analizi başlatılıyor ({self.current_provider})...")
            
            # Get prompt template
            prompt_template = self._get_prompt_for_analysis_type(analysis_type)
            
            # AI analizi
            if progress_callback:
                progress_callback(0.8, "Metin analiz ediliyor...")
                
            analyzed_text = await self.ai_service_manager.analyze_text(
                extracted_text,
                self.current_provider,
                prompt_template
            )
            
            # İlerleme bildirimi
            if progress_callback:
                progress_callback(0.95, "Analiz tamamlandı, sonuçlar hazırlanıyor...")
            
            result = ProcessingResult(
                original_text=extracted_text,
                analyzed_text=analyzed_text,
                metadata=metadata,
                timestamp=datetime.now(),
                file_name=os.path.basename(file_path),
                analysis_type=analysis_type
            )
            
            # Save to history
            if self.history_repo:
                try:
                    self.history_repo.save_analysis(result, self.current_provider)
                    if progress_callback:
                        progress_callback(0.98, "Analiz geçmişe kaydedildi")
                except Exception as e:
                    print(f"Geçmiş kaydedilirken hata: {str(e)}")
            
            # skip_result_callback'e göre sonucu göster
            if not skip_result_callback and self._on_processing_complete:
                self._on_processing_complete(result)
                
            return result
                
        except Exception as e:
            self._update_status(f"Hata: {str(e)}")
            if self._on_error:
                self._on_error(str(e))
            return None
            
        finally:
            if self._on_progress_stop:
                self._on_progress_stop()

    def _update_status(self, status: str):
        """Update processing status"""
        self.processing_status = status
        if self._on_status_changed:
            self._on_status_changed(status)
    
    def set_ai_provider(self, provider: str):
        """Set current AI provider"""
        self.current_provider = provider
    
    def _get_prompt_for_analysis_type(self, analysis_type: str) -> str:
        """Analiz tipine göre uygun prompt'u döndür"""
        return AnalysisPrompts.get_prompt(
            analysis_type,
            custom_analysis_repo=self.custom_analysis_repo if hasattr(self, 'custom_analysis_repo') else None
        )
    
    def add_recent_file(self, file_path: str, analysis_type: str):
        """Add file to recent files list"""
        try:
            recent_files = self.get_recent_files()
            # Dosya zaten listedeyse çıkar (sonra başa ekleyeceğiz)
            recent_files = [f for f in recent_files if f["path"] != file_path]
            # Başa ekle
            recent_files.insert(0, {
                "path": file_path,
                "name": os.path.basename(file_path),
                "analysis_type": analysis_type,
                "date": datetime.now().isoformat()
            })
            # Max 10 dosya sakla
            recent_files = recent_files[:10]
            # Kaydet
            self._save_recent_files(recent_files)
        except Exception as e:
            print(f"Son dosyalar kaydedilirken hata: {str(e)}")

    def get_recent_files(self) -> list:
        """Get recent files list"""
        try:
            recent_files_path = os.path.join("data", "recent_files.json")
            if os.path.exists(recent_files_path):
                with open(recent_files_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Son dosyalar yüklenirken hata: {str(e)}")
        return []
        
    def _save_recent_files(self, recent_files: list):
        """Save recent files list"""
        try:
            os.makedirs("data", exist_ok=True)
            recent_files_path = os.path.join("data", "recent_files.json")
            with open(recent_files_path, 'w', encoding='utf-8') as f:
                json.dump(recent_files, f, ensure_ascii=False)
        except Exception as e:
            print(f"Son dosyalar kaydedilirken hata: {str(e)}")

    def save_file_processing_settings(self, settings: dict):
        """Save file processing settings"""
        try:
            self.processing_setting.update(settings)
            self._save_settings()
            
            if self._on_settings_saved:
                self._on_settings_saved()
                
        except Exception as e:
            if self._on_error:
                self._on_error(str(e))

    async def analyze_text(self, text: str, analysis_type: str) -> ProcessingResult:
        """Analyze text directly using AI"""
        try:
            print(f"Metin analizi başlatılıyor, uzunluk: {len(text)}, analiz tipi: {analysis_type}")
            
            # Get prompt template for analysis type
            prompt_template = self._get_prompt_for_analysis_type(analysis_type)
            
            # Send to AI service
            print(f"AI servisi çağrılıyor ({self.current_provider})...")
            analyzed_text = await self.ai_service_manager.analyze_text(
                text,
                self.current_provider,
                prompt_template
            )
            print(f"AI servisi yanıt verdi, uzunluk: {len(analyzed_text)}")
            
            # Create result
            result = ProcessingResult(
                original_text=text,
                analyzed_text=analyzed_text,
                metadata={},
                timestamp=datetime.now(),
                file_name="Doğrudan Metin Analizi",
                analysis_type=analysis_type
            )
            
            if self._on_processing_complete:
                self._on_processing_complete(result)
                
            return result
                
        except Exception as e:
            print(f"Metin analizi hatası: {str(e)}")
            if self._on_error:
                self._on_error(str(e))
            raise

    