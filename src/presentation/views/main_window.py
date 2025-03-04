import os
import customtkinter as ctk
from tkinter import messagebox
import asyncio
import threading
import datetime
from typing import List, Optional

from src.services.file_processing.file_processor_factory import FileProcessorFactory
from src.services.file_processing.result_manager import ProcessingResult, ResultManager
from src.presentation.viewmodels.main_viewmodel import MainViewModel
from .components.file_drop_area import FileDropArea
from .components.sidebar import Sidebar
from .components.status_bar import StatusBar
from .result_window import ResultWindow
from .analysis_options_window import AnalysisOptionsWindow
from .file_splitting_window import FileSplittingWindow
from .combine_options_window import CombineOptionsWindow
from .file_processing_settings_dialog import FileProcessingSettingsDialog
from .components.icons import get_gear_icon
from src.presentation.themes.theme_manager import ThemeManager

# İçe aktarılacak sekme içerikleri için ön tanımlamalar
from .settings_content import SimplifiedSettingsContent
from .history_content import HistoryContent
from .custom_analysis_content import CustomAnalysisContent 
from .prompt_manager_content import PromptManagerContent

class MainWindow(ctk.CTk):
    def __init__(self, viewmodel: MainViewModel):
        super().__init__()
        
        # Core components
        self.viewmodel = viewmodel
        self.file_processor_factory = FileProcessorFactory()
        self.result_manager = ResultManager()
        
        # State
        self.selected_files: List[str] = []
        self.current_analysis_type: Optional[str] = None

        # Database session (initially None, will be set by Application)
        self.session = None

         # State
        self.selected_files: List[str] = []
        self.current_analysis_type: Optional[str] = None
        
        # Set callbacks
        self.viewmodel.set_callbacks(
            on_processing_complete=self._show_results,
            on_status_changed=self._update_status,
            on_progress_start=self._start_progress,
            on_progress_stop=self._stop_progress,
            on_error=self._show_error
        )

        # Theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize UI
        self._init_ui()

        # Apply current theme
        self.theme_manager.apply_theme(self.theme_manager.current_theme)
        
        # Store tab instances
        self.tab_instances = {}

    def _init_ui(self):
        """Initialize user interface"""
        # Configure window
        self.title("AI Metin Analizcisi")
        self.geometry("1200x800")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create layout
        self._create_layout()
    
    def _create_layout(self):
        """Create the main layout"""
        # Create main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.sidebar = Sidebar(
            self,
            on_analysis_type_changed=self._on_analysis_type_changed,
            on_ai_provider_changed=self._on_ai_provider_changed,
            on_settings_clicked=self._show_settings_tab,
            on_history_clicked=self._show_history_tab,
            on_custom_analysis_clicked=self._show_custom_analysis_tab,
            on_template_manager_clicked=self._show_template_manager_tab
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Create tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
            # Create tabs
        self.analysis_tab = self.tab_view.add("Analiz")
        print(f"Analiz tab oluşturuldu: {self.analysis_tab}")
        
        self.settings_tab = self.tab_view.add("Ayarlar")
        print(f"Ayarlar tab oluşturuldu: {self.settings_tab}")
        
        self.history_tab = self.tab_view.add("Geçmiş")
        print(f"Geçmiş tab oluşturuldu: {self.history_tab}")
        
        self.custom_analysis_tab = self.tab_view.add("Özel Analiz Türleri")
        print(f"Özel Analiz tab oluşturuldu: {self.custom_analysis_tab}")
        
        self.template_manager_tab = self.tab_view.add("Şablon Yöneticisi")
        print(f"Şablon tab oluşturuldu: {self.template_manager_tab}")
        
        # Initially show only the analysis tab
        self.tab_view.set("Analiz")
        
        # Hide other tabs initially
        for tab_name in ["Ayarlar", "Geçmiş", "Özel Analiz Türleri", "Şablon Yöneticisi"]:
            self.tab_view._segmented_button.configure(
                corner_radius=0, border_width=1, 
                fg_color="#2b2b2b", selected_color="#1f538d"
            )
            if hasattr(self.tab_view._segmented_button, "configure_tab"):
                self.tab_view._segmented_button.configure_tab(tab_name, state="hidden")
        
        # Setup analysis tab content
        self.analysis_tab.grid_columnconfigure(0, weight=1)
        self.analysis_tab.grid_rowconfigure(2, weight=1)
        
        # Create file drop area
        self.file_drop = FileDropArea(
            self.analysis_tab,
            on_file_drop=self._handle_file_select
        )
        self.file_drop.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self._create_file_info_frame()
        
        # Create text display
        self.text_display = ctk.CTkTextbox(
            self.analysis_tab,
            wrap="word",
            font=("Arial", 12)
        )
        self.text_display.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Create status bar
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Initialize other tabs (but don't create content yet - we'll do lazy loading)
        self.settings_content = None
        self.history_content = None
        self.custom_analysis_content = None
        self.prompt_manager_content = None

    def set_session(self, session):
        """Set the database session and update components"""
        self.session = session
        self.sidebar.session = session  # Pass session to sidebar
        
        # Reload sidebar custom analysis types 
        self.sidebar._load_custom_analysis_types()

    def _show_settings_tab(self):
        """Show the settings tab"""
        try:
            # Lazy load the settings content
            if not self.settings_content:
                print("Settings content yükleniyor...")
                self.settings_content = SimplifiedSettingsContent(self.settings_tab, self)
                self.settings_content.pack(fill="both", expand=True)
                print("Settings content yüklendi")
            
            # Make the tab visible if it's not
            if hasattr(self.tab_view._segmented_button, "configure_tab"):
                print("Tab görünür yapılıyor...")
                self.tab_view._segmented_button.configure_tab("Ayarlar", state="normal")
                print("Tab görünür yapıldı")
            
            # Switch to the tab
            print("Tab'a geçiliyor...")
            self.tab_view.set("Ayarlar")
            print("Tab'a geçildi")
        except Exception as e:
            print(f"Ayarlar sekmesi gösterilirken hata: {str(e)}")
            import traceback
            traceback.print_exc()

    def _show_history_tab(self):
        """Show the history tab"""
        # Lazy load the history content
        if not self.history_content:
            from src.repositories.history_repository import HistoryRepository
            from src.models.history import AnalysisHistory
            
            if hasattr(self, 'session'):
                history_repo = HistoryRepository(self.session, AnalysisHistory)
                self.history_content = HistoryContent(self.history_tab, history_repo)
                self.history_content.pack(fill="both", expand=True)
            else:
                messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı.")
                return
        
        # Make the tab visible if it's not
        if hasattr(self.tab_view._segmented_button, "configure_tab"):
            self.tab_view._segmented_button.configure_tab("Geçmiş", state="normal")
        
        # Switch to the tab
        self.tab_view.set("Geçmiş")

    def _show_custom_analysis_tab(self):
        """Show the custom analysis tab"""
        # Lazy load the custom analysis content
        if not self.custom_analysis_content:
            from src.repositories.custom_analysis_repository import CustomAnalysisRepository
            from src.models.custom_analysis_type import CustomAnalysisType
            
            if hasattr(self, 'session'):
                analysis_repo = CustomAnalysisRepository(self.session, CustomAnalysisType)
                self.custom_analysis_content = CustomAnalysisContent(
                    self.custom_analysis_tab, 
                    analysis_repo,
                    on_types_changed=self.sidebar._update_analysis_types
                )
                self.custom_analysis_content.pack(fill="both", expand=True)
            else:
                messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı.")
                return
        
        # Make the tab visible if it's not
        if hasattr(self.tab_view._segmented_button, "configure_tab"):
            self.tab_view._segmented_button.configure_tab("Özel Analiz Türleri", state="normal")
        
        # Switch to the tab
        self.tab_view.set("Özel Analiz Türleri")

    def _show_template_manager_tab(self):
        """Show the template manager tab"""
        # Lazy load the template manager content
        if not self.prompt_manager_content:
            self.prompt_manager_content = PromptManagerContent(self.template_manager_tab, self)
            self.prompt_manager_content.pack(fill="both", expand=True)
        
        # Make the tab visible if it's not
        if hasattr(self.tab_view._segmented_button, "configure_tab"):
            self.tab_view._segmented_button.configure_tab("Şablon Yöneticisi", state="normal")
        
        # Switch to the tab
        self.tab_view.set("Şablon Yöneticisi")
    
    def _handle_file_select(self, file_paths: List[str]):
        """Handle file selection"""
        self.selected_files = file_paths
        
        # Update recent files
        if len(file_paths) == 1:
            self.viewmodel.add_recent_file(
                file_paths[0], 
                self.sidebar.get_analysis_type()
            )
        
        # Update file label
        if len(file_paths) == 1:
            self.file_label.configure(text=os.path.basename(file_paths[0]))
        else:
            self.file_label.configure(text=f"{len(file_paths)} dosya seçildi")
        
        # Enable analyze button
        self.analyze_button.configure(state="normal")
        
        # Switch to analysis tab
        self.tab_view.set("Analiz")

    def _create_file_info_frame(self):
        """Create file info frame with buttons"""
        self.file_info_frame = ctk.CTkFrame(self.analysis_tab)
        self.file_info_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        # Selected file label
        self.file_label = ctk.CTkLabel(
            self.file_info_frame,
            text="Dosya seçilmedi",
            font=("Arial", 12)
        )
        self.file_label.pack(side="left", padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.file_info_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10)

        # Quick settings button
        self.settings_button = ctk.CTkButton(
            buttons_frame,
            text="Parçalama",
            width=80,
            height=32,
            fg_color="#28a745",
            hover_color="#218838",
            command=self._show_quick_settings
        )
        self.settings_button.pack(side="left", padx=(0, 10))
        
        # Analyze button
        self.analyze_button = ctk.CTkButton(
            buttons_frame,
            text="Analiz Et",
            font=("Arial", 12, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            command=self._start_analysis,
            state="disabled"
        )
        self.analyze_button.pack(side="left")

    def _process_single_file(self, file_path: str):
        """Process a single file"""
        try:
            # Dosya uzantısını kontrol et
            ext = os.path.splitext(file_path)[1].lower()
            
            # Eğer görüntü dosyasıysa ve Tesseract kurulu değilse uyarı göster
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'] and not self._check_tesseract_installed():
                self.text_display.configure(state="normal")
                self.text_display.delete("1.0", "end")
                self.text_display.insert("1.0", "Görüntü dosyası seçildi, ancak Tesseract OCR kurulu değil!\n\n")
                self.text_display.insert("end", "Görüntü dosyalarını analiz edebilmek için Tesseract OCR'ı kurmanız gerekmektedir:\n\n")
                self.text_display.insert("end", "1. https://github.com/UB-Mannheim/tesseract/wiki adresinden indirin\n")
                self.text_display.insert("end", "2. Kurulum sırasında 'Add to PATH' seçeneğini işaretleyin\n")
                self.text_display.insert("end", "3. Kurulum tamamlandıktan sonra uygulamayı yeniden başlatın\n\n")
                self.text_display.insert("end", "Kurulum sonrası, görüntüdeki metinler otomatik olarak tanınacak ve analiz edilebilecektir.")
                self.text_display.configure(state="disabled")
                
                # Ayrıca bir mesaj kutusu göster
                messagebox.showwarning(
                    "Tesseract OCR Gerekli", 
                    "Görüntü dosyalarını analiz etmek için Tesseract OCR kurulumu gereklidir.\n\n"
                    "1. https://github.com/UB-Mannheim/tesseract/wiki adresinden indirin\n"
                    "2. Kurulum sırasında 'Add to PATH' seçeneğini işaretleyin\n"
                    "3. Uygulamayı yeniden başlatın"
                )
                return
            
            # Start progress
            self.status_bar.start_progress()
            
            # Update status and text display
            status_msg = f"Dosya işleniyor: {os.path.basename(file_path)}"
            self.status_bar.set_status(status_msg)
            
            # Metin alanını temizle ve işlem bilgisi göster
            self.text_display.configure(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("1.0", f"İşlem başlatılıyor: {os.path.basename(file_path)}\n")
            self.text_display.configure(state="disabled")
            
            # Start processing in background
            threading.Thread(
                target=self._process_file_async,
                args=(file_path,)
            ).start()
            
        except Exception as e:
            self.status_bar.stop_progress()
            self._show_error(f"Dosya işlenirken hata: {str(e)}")

    def update_progress_text(self, message: str):
        """Update the progress text in the text display"""
        self.text_display.configure(state="normal")
        self.text_display.insert("end", f"\n> {message}")
        self.text_display.see("end")  # Otomatik kaydırma
        self.text_display.configure(state="disabled")
        self.update()  # UI'yi güncelle


    def _process_file_async(self, file_path: str):
        """Process file asynchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            analysis_type = self.sidebar.get_analysis_type()
            
            # Dosya uzantısını al
            ext = os.path.splitext(file_path)[1].lower()
            
            # Görüntü dosyası için özel ilerleme mesajları
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
                self.after(0, lambda: self.update_progress_text("Görüntü dosyası işleniyor..."))
                self.after(100, lambda: self.update_progress_text("Tesseract OCR ile metin tanıma başlatılıyor..."))
                self.after(300, lambda: self.update_progress_text("Bu işlem, görüntünün boyutuna ve karmaşıklığına bağlı olarak biraz zaman alabilir..."))
            else:
                self.after(0, lambda: self.update_progress_text(f"Dosya türü: {ext}"))
            
            # İlerlemeyi güncelle - Metin çıkarılıyor
            self.after(500, lambda: self.update_progress_text("Dosyadan metin çıkarılıyor..."))
            
            # İlerlemeyi güncelle - AI sağlayıcı
            provider = self.sidebar.get_ai_provider()
            self.after(700, lambda: self.update_progress_text(f"Yapay zeka sağlayıcı: {provider.upper()}"))
            
            # İlerlemeyi güncelle - Analiz türü
            self.after(800, lambda: self.update_progress_text(f"Analiz türü: {analysis_type}"))
            
            # İlerlemeyi güncelle - Yapay zekaya gönderiliyor
            self.after(1000, lambda: self.update_progress_text("Yapay zeka hizmetine gönderiliyor..."))
            
            # Dosyayı işle
            result = loop.run_until_complete(
                self.viewmodel.process_file(
                    file_path, 
                    analysis_type,
                    progress_callback=self._update_processing_progress,
                    skip_result_callback=True
                )
            )
            
            if result:
                # İlerlemeyi güncelle - Tamamlandı
                self.after(0, lambda: self.update_progress_text("Analiz tamamlandı! Sonuçlar gösteriliyor..."))
                self.after(100, lambda: self._show_results(result))
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.update_progress_text(f"HATA: {error_msg}"))
            self.after(100, lambda: self._show_error(f"Dosya işleme hatası: {error_msg}"))
        finally:
            loop.close()
            self.after(0, self.status_bar.stop_progress)

    def _update_processing_progress(self, progress: float, message: str):
        """Update processing progress from callback"""
        self.after(0, lambda: self.update_progress_text(message))

    def _show_analysis_options(self, file_paths: List[str]):
        """Show analysis options for multiple files"""
        options_window = AnalysisOptionsWindow(
            self,
            file_paths,
            on_option_selected=self._start_analysis_with_option
        )
        options_window.grab_set()

    def _show_splitting_options(self, file_path: str):
        """Show splitting options for large files"""
        options_window = FileSplittingWindow(
            self,
            file_path,
            on_split_selected=self._start_split_analysis
        )
        options_window.grab_set()

    def _start_analysis_with_option(self, file_paths: List[str], combine_results: bool):
        """Start analysis with selected option"""
        analysis_type = self.sidebar.get_analysis_type()
        
        if combine_results:
            threading.Thread(
                target=self._process_files_combined_async,
                args=(file_paths, analysis_type)
            ).start()
        else:
            self._process_files_separate(file_paths, analysis_type)

    def _process_files_combined_async(self, file_paths: List[str], analysis_type: str):
        """Process multiple files and combine results"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.after(0, self.status_bar.start_progress)
            results = []
            
            # İlerleme bildirimi
            self.after(0, lambda: self.update_progress_text(f"Toplam {len(file_paths)} dosya işlenecek ve birleştirilecek"))
            
            for i, file_path in enumerate(file_paths):
                # İlerleme bildirimi
                status_msg = f"Dosya işleniyor ({i+1}/{len(file_paths)}): {os.path.basename(file_path)}"
                self.after(0, lambda msg=status_msg: self.update_progress_text(msg))
                self.after(0, lambda msg=status_msg: self.status_bar.set_status(msg))
                
                # Dosyayı işle - ama sonuçları gösterme (skip_result_callback=True)
                result = loop.run_until_complete(
                    self.viewmodel.process_file(
                        file_path, 
                        analysis_type,
                        skip_result_callback=True  # Sonuçları gösterme
                    )
                )
                
                if result:
                    results.append(result)
                    self.after(0, lambda: self.update_progress_text(f"Dosya analizi tamamlandı: {os.path.basename(file_path)}"))
            
            if results:
                self.after(0, lambda: self.update_progress_text(f"Tüm dosyalar işlendi ({len(results)}/{len(file_paths)}). Birleştirme seçenekleri gösteriliyor..."))
                self.after(0, lambda: self._show_combine_options(results))
                
        except Exception as e:
            self.after(0, lambda: self.update_progress_text(f"HATA: {str(e)}"))
            self.after(0, lambda: self._show_error(f"Dosyalar işlenirken hata: {str(e)}"))
        finally:
            loop.close()
            self.after(0, self.status_bar.stop_progress)

    def _process_files_async(self, file_paths: List[str], analysis_type: str):
        """Process files separately asynchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.after(0, self.status_bar.start_progress)
            
            # İlerleme bildirimi
            self.after(0, lambda: self.update_progress_text(f"Toplam {len(file_paths)} dosya ayrı ayrı işlenecek"))
            
            for i, file_path in enumerate(file_paths):
                # İlerleme bildirimi
                status_msg = f"Dosya işleniyor ({i+1}/{len(file_paths)}): {os.path.basename(file_path)}"
                self.after(0, lambda msg=status_msg: self.update_progress_text(msg))
                self.after(0, lambda msg=status_msg: self.status_bar.set_status(msg))
                
                # Dosyayı işle ve hemen sonuçları göster
                result = loop.run_until_complete(
                    self.viewmodel.process_file(
                        file_path, 
                        analysis_type,
                        skip_result_callback=False  # Sonuçları hemen göster
                    )
                )
                
                self.after(0, lambda: self.update_progress_text(f"Dosya analizi tamamlandı: {os.path.basename(file_path)}"))
            
            self.after(0, lambda: self.update_progress_text(f"Tüm dosyaların işlenmesi tamamlandı."))
                
        except Exception as e:
            self.after(0, lambda: self.update_progress_text(f"HATA: {str(e)}"))
            self.after(0, lambda: self._show_error(f"Dosyalar işlenirken hata: {str(e)}"))
        finally:
            loop.close()
            self.after(0, self.status_bar.stop_progress)

    def _process_files_async(self, file_paths: List[str], analysis_type: str):
        """Process files separately asynchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.after(0, self.status_bar.start_progress)
            
            for i, file_path in enumerate(file_paths):
                self.after(0, lambda msg=f"Dosya işleniyor ({i+1}/{len(file_paths)}): {os.path.basename(file_path)}":
                          self.status_bar.set_status(msg))
                
                result = loop.run_until_complete(
                    self.viewmodel.process_file(file_path, analysis_type)
                )
                
                if result:
                    self.after(0, lambda r=result: self._show_results(r))
            
        except Exception as e:
            self.after(0, lambda: self._show_error(f"Dosyalar işlenirken hata: {str(e)}"))
        finally:
            loop.close()
            self.after(0, self.status_bar.stop_progress)

    def _start_split_analysis(self, file_path: str, options: dict):
        """Start analysis with file splitting"""
        threading.Thread(
            target=self._process_split_file_async,
            args=(file_path, options)
        ).start()

    def _process_split_file_async(self, file_path: str, options: dict):
        """Process split file asynchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            self.after(0, self.status_bar.start_progress)
            analysis_type = self.sidebar.get_analysis_type()
            
            # Split file
            processor = self.file_processor_factory.get_processor(file_path)
            chunks = processor.split_file(
                file_path,
                chunk_size=options['chunk_size'],
                method="page"
            )
            
            results = []
            for i, chunk in enumerate(chunks):
                self.after(0, lambda msg=f"Parça işleniyor ({i+1}/{len(chunks)})":
                          self.status_bar.set_status(msg))
                
                result = loop.run_until_complete(
                    self.viewmodel.analyze_text(chunk, analysis_type)
                )
                if result:
                    results.append(result)
            
            if options['combine_results'] and results:
                combined = self.result_manager.combine_results(results, "sequential")
                self.after(0, lambda: self._show_results(combined))
            else:
                for result in results:
                    self.after(0, lambda r=result: self._show_results(r))
                    
        except Exception as e:
            self.after(0, lambda: self._show_error(f"Dosya bölme işlemi başarısız: {str(e)}"))
        finally:
            loop.close()
            self.after(0, self.status_bar.stop_progress)

    def _show_combine_options(self, results: List[ProcessingResult]):
        """Show combine options window"""
        options_window = CombineOptionsWindow(
            self,
            len(results),
            on_option_selected=lambda combo_type: self._combine_and_show_results(results, combo_type)
        )
        options_window.grab_set()

    def _combine_and_show_results(self, results: List[ProcessingResult], combination_type: str):
        """Combine results and show"""
        try:
            combined = self.result_manager.combine_results(results, combination_type)
            self._show_results(combined)
        except Exception as e:
            self._show_error(f"Sonuçlar birleştirilirken hata oluştu: {str(e)}")

    def _show_results(self, result: ProcessingResult):
        """Show results window"""
        # Sonuç için benzersiz bir ID oluştur
        result_id = f"{result.file_name}_{result.timestamp.strftime('%Y%m%d%H%M%S')}"
        
        # Eğer bu sonuç zaten gösterilmişse tekrar gösterme
        if hasattr(self, '_last_shown_result') and self._last_shown_result == result_id:
            print(f"Bu sonuç zaten gösterildi: {result_id}")
            return
        
        # Son gösterilen sonucu kaydet
        self._last_shown_result = result_id
        
        # Sonuç penceresini göster
        ResultWindow(self, result)

    def _show_error(self, error: str):
        """Show error dialog"""
        messagebox.showerror("Hata", error)
        self.analyze_button.configure(state="normal", text="Analiz Et")

    def _start_progress(self):
        """Start progress indicator"""
        self.status_bar.start_progress()

    def _stop_progress(self):
        """Stop progress indicator"""
        self.status_bar.stop_progress()

    def _update_status(self, status: str):
        """Update status bar"""
        self.status_bar.set_status(status)

    def _on_analysis_type_changed(self, analysis_type: str):
        """Handle analysis type change"""
        self.current_analysis_type = analysis_type

    def _on_ai_provider_changed(self, provider: str):
        """Handle AI provider change"""
        self.viewmodel.set_ai_provider(provider)

    def _start_analysis(self):
        """Start analysis when button is clicked"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin.")
            return
        
        if len(self.selected_files) > 1:
            # Çoklu dosya için seçenekler
            self._show_analysis_options(self.selected_files)
        else:
            # Tek dosya için boyut kontrolü ve parçalama
            file_size = os.path.getsize(self.selected_files[0])
            if file_size > 1_000_000:  # 1MB üzeri dosyalar için
                self._show_splitting_options(self.selected_files[0])
            else:
                self._process_single_file(self.selected_files[0])

    def _show_quick_settings(self):
        """Show quick settings dialog"""
        dialog = FileProcessingSettingsDialog(
            self, 
            current_settings=self.viewmodel.get_processing_settings()
        )
        
        # Wait for dialog result
        self.wait_window(dialog)
        
        # Update settings if dialog was not cancelled
        if dialog.result:
            self.viewmodel.update_processing_settings(dialog.result)

    def _create_recent_files_menu(self):
        """Create recent files menu"""
        recent_files_frame = ctk.CTkFrame(self.content)
        recent_files_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        recent_label = ctk.CTkLabel(
            recent_files_frame,
            text="Son Kullanılan Dosyalar",
            font=("Arial", 12, "bold")
        )
        recent_label.pack(anchor="w", padx=10, pady=5)
        
        recent_files = self.viewmodel.get_recent_files()
        if not recent_files:
            no_files_label = ctk.CTkLabel(
                recent_files_frame,
                text="Henüz dosya geçmişi yok",
                text_color="gray"
            )
            no_files_label.pack(padx=20, pady=5)
            return
        
        for file in recent_files[:5]:  # Show last 5 files
            file_frame = ctk.CTkFrame(recent_files_frame, fg_color="transparent")
            file_frame.pack(fill="x", padx=20, pady=2)
            
            file_button = ctk.CTkButton(
                file_frame,
                text=file["name"],
                anchor="w",
                font=("Arial", 11),
                fg_color="transparent",
                text_color=self.theme_manager.get_color("text_color"),
                hover_color=self.theme_manager.get_color("button_hover_color"),
                command=lambda p=file["path"]: self._handle_file_select([p])
            )
            file_button.pack(side="left", fill="x", expand=True)
            
            date = datetime.fromisoformat(file["date"]).strftime("%d.%m.%Y %H:%M")
            date_label = ctk.CTkLabel(
                file_frame,
                text=date,
                font=("Arial", 10),
                text_color="gray"
            )
            date_label.pack(side="right", padx=10)

    def _check_tesseract_installed(self):
        """Tesseract'ın kurulu olup olmadığını kontrol et"""
        try:
            import pytesseract
            # Tesseract versiyonunu almaya çalışarak kurulu olup olmadığını kontrol et
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            print(f"Tesseract kontrolünde hata: {str(e)}")
            return False