import customtkinter as ctk
from typing import Callable, Optional

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, 
                on_analysis_type_changed: Optional[Callable] = None, 
                on_ai_provider_changed: Optional[Callable] = None,
                on_settings_clicked: Optional[Callable] = None,
                on_history_clicked: Optional[Callable] = None,
                on_custom_analysis_clicked: Optional[Callable] = None,
                on_template_manager_clicked: Optional[Callable] = None,
                **kwargs):
        super().__init__(master, width=200, corner_radius=0, fg_color="#2b2b2b", **kwargs)
        
        self.on_analysis_type_changed = on_analysis_type_changed
        self.on_ai_provider_changed = on_ai_provider_changed
        self.on_settings_clicked = on_settings_clicked
        self.on_history_clicked = on_history_clicked
        self.on_custom_analysis_clicked = on_custom_analysis_clicked
        self.on_template_manager_clicked = on_template_manager_clicked

        # Session başlangıçta None, daha sonra set edilecek
        self.session = None

        self.analysis_types = ["Özet", "Soru-Cevap", "Anahtar Noktalar", "Çeviri", 
                             "Analiz", "Teknik Analiz", "Özet Rapor"]   

        # Create sidebar elements
        self._create_widgets()

        # Sonra özel analiz türlerini yükle
        self._update_analysis_types()
        self._load_custom_analysis_types()
    
    def _create_widgets(self):
        """Create sidebar widgets"""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="AI Metin Analizcisi",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=20, padx=10)
        
        # AI Model Selection
        self.model_label = ctk.CTkLabel(
            self,
            text="AI Modeli:",
            font=("Arial", 12)
        )
        self.model_label.pack(pady=(20, 5), padx=10, anchor="w")
        
        self.model_combobox = ctk.CTkComboBox(
            self,
            values=["OpenAI", "Gemini","Claude","Deepseek"],
            width=180,
            command=self._on_model_changed
        )
        self.model_combobox.pack(pady=(0, 20), padx=10)
        
        # Analysis Type Selection
        self.analysis_label = ctk.CTkLabel(
            self,
            text="Analiz Tipi:",
            font=("Arial", 12)
        )
        self.analysis_label.pack(pady=(20, 5), padx=10, anchor="w")
        
        self.analysis_combobox = ctk.CTkComboBox(
            self,
            values=self.analysis_types,  # Başlangıçta standart tipler
            width=180,
            command=self._on_analysis_changed
        )
        self.analysis_combobox.pack(pady=(0, 20), padx=10)
        
        # Settings Button
        self.settings_button = ctk.CTkButton(
            self,
            text="Ayarlar",
            width=180,
            command=self._open_settings
        )
        self.settings_button.pack(pady=20, padx=10)

        # Şablon Yöneticisi butonu
        self.template_button = ctk.CTkButton(
            self,
            text="Şablon Yöneticisi",
            width=180,
            command=self._open_template_manager
        )
        self.template_button.pack(pady=10, padx=10)

        # Geçmiş butonu
        self.history_button = ctk.CTkButton(
            self,
            text="Analiz Geçmişi",
            width=180,
            command=self._open_history
        )
        self.history_button.pack(pady=10, padx=10)

        # Özel Analiz Türleri butonu
        self.custom_analysis_button = ctk.CTkButton(
            self,
            text="Özel Analiz Türleri",
            width=180,
            command=self._open_custom_analysis
        )
        self.custom_analysis_button.pack(pady=10, padx=10)

    def get_analysis_type(self) -> str:
        """Get selected analysis type"""
        return self.analysis_combobox.get()
    
    def get_ai_provider(self) -> str:
        """Get selected AI provider"""
        provider_map = {
            "OpenAI": "openai",
            "Gemini": "gemini",
            "Claude": "claude",
            "Deepseek": "deepseek"
        }
        return provider_map[self.model_combobox.get()]
    
    def _on_model_changed(self, value):
        """Handle model change"""
        if self.on_ai_provider_changed:
            self.on_ai_provider_changed(self.get_ai_provider())
    
    def _on_analysis_changed(self, value):
        """Handle analysis type change"""
        if self.on_analysis_type_changed:
            self.on_analysis_type_changed(value)
            
    def _open_settings(self):
        """Open settings tab"""
        if self.on_settings_clicked:
            self.on_settings_clicked()

    def _open_template_manager(self):
        """Open template manager tab"""
        if self.on_template_manager_clicked:
            self.on_template_manager_clicked()

    def _open_history(self):
        """Open history tab"""
        if self.on_history_clicked:
            self.on_history_clicked()

    def _open_custom_analysis(self):
        """Open custom analysis types tab"""
        if self.on_custom_analysis_clicked:
            self.on_custom_analysis_clicked()

    def _update_analysis_types(self):
        """Update analysis types in combobox"""
        try:
            from src.repositories.custom_analysis_repository import CustomAnalysisRepository
            from src.models.custom_analysis_type import CustomAnalysisType
            
            # Session kontrolü
            if self.session is None:
                print("Session bulunamadı - _update_analysis_types")
                app = self.winfo_toplevel()
                if hasattr(app, 'session') and app.session is not None:
                    self.session = app.session
                else:
                    print("Ana pencerede de session bulunamadı - güncelleme yapılamıyor")
                    return
            
            # Repository oluştur
            analysis_repo = CustomAnalysisRepository(self.session, CustomAnalysisType)
            
            # Standart analiz tipleri
            standard_types = ["Özet", "Soru-Cevap", "Anahtar Noktalar", "Çeviri", 
                            "Analiz", "Teknik Analiz", "Özet Rapor"]
            
            # Özel analiz tiplerini al
            custom_types = analysis_repo.get_all_names()
            print(f"Güncellenmiş özel tipler: {custom_types}")
            
            # Combobox'ı güncelle
            all_types = standard_types + custom_types
            self.analysis_combobox.configure(values=all_types)
            print("Combobox güncellendi - _update_analysis_types")
                
        except Exception as e:
            print(f"Analiz türleri güncellenirken hata: {str(e)}")
            import traceback
            traceback.print_exc()

    def _load_custom_analysis_types(self):
        """Özel analiz türlerini yükle"""
        try:
            # Doğrudan session kontrolü yap
            if self.session is None:
                print("Session bulunamadı - doğrudan Sidebar.session")
                
                # Ana pencereden almayı dene
                app = self.winfo_toplevel()
                if hasattr(app, 'session') and app.session is not None:
                    self.session = app.session
                    print("Session ana pencereden alındı")
                else:
                    print("Ana pencerede de session bulunamadı")
                    return
                    
            from src.repositories.custom_analysis_repository import CustomAnalysisRepository
            from src.models.custom_analysis_type import CustomAnalysisType
            
            print(f"Session kullanılarak repository oluşturuluyor: {self.session}")
            custom_repo = CustomAnalysisRepository(self.session, CustomAnalysisType)
            custom_types = custom_repo.get_all_names()
            
            print(f"Yüklenen özel tipler: {custom_types}")  # Debug için
            
            # Mevcut analiz tiplerine özel tipleri ekle
            if custom_types:
                # Standart tipleri al
                standard_types = ["Özet", "Soru-Cevap", "Anahtar Noktalar", "Çeviri", 
                                "Analiz", "Teknik Analiz", "Özet Rapor"]
                
                # Tüm tipleri birleştir
                all_types = standard_types + custom_types
                self.analysis_types = all_types  # Güncelle
                
                # Combobox değerlerini güncelle
                if hasattr(self, 'analysis_combobox'):
                    self.analysis_combobox.configure(values=all_types)
                    print("Combobox güncellendi")
                    
        except Exception as e:
            print(f"Özel analiz türleri yüklenirken hata: {str(e)}")
            import traceback
            traceback.print_exc()  # Detaylı hata çıktısı