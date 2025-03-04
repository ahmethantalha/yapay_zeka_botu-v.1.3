import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
from src.presentation.viewmodels.main_viewmodel import MainViewModel
from .prompt_template_window import PromptTemplateWindow

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, viewmodel: MainViewModel):  
        super().__init__(parent)
        
        self.viewmodel = viewmodel
        self.lift()
        self.focus_force()
        
        self.center_window()
        
        # Configure window
        self.title("Ayarlar")
        self.geometry("800x700")
        self.resizable(False, False)
        
        # Set callbacks
        self.viewmodel.set_callbacks(
            on_settings_saved=self._on_settings_saved,
            on_error=self._show_error
        )
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add tabs
        self.ai_tab = self.tabview.add("AI Ayarları")
        self.appearance_tab = self.tabview.add("Görünüm")
        self.file_processing_tab = self.tabview.add("Dosya İşleme")
        self.prompt_tab = self.tabview.add("Promptlar")
        
        # Create tab contents
        self._create_ai_settings()
        self._create_file_processing_settings()  # Aktif ettik
        self._create_prompt_settings()
        self._create_appearance_settings()
        
        # Create save button
        self.save_button = ctk.CTkButton(
            self,
            text="Ayarları Kaydet",
            command=self._save_settings
        )
        self.save_button.pack(pady=20)
    
    def _create_ai_settings(self):
        """Create AI settings tab content"""
        # OpenAI Settings
        self.openai_frame = ctk.CTkFrame(self.ai_tab)
        self.openai_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            self.openai_frame,
            text="OpenAI Ayarları",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.openai_key = ctk.CTkEntry(
            self.openai_frame,
            placeholder_text="OpenAI API Key",
            width=300
        )
        self.openai_key.pack(pady=5)
        
        self.openai_model = ctk.CTkComboBox(
            self.openai_frame,
            values=["gpt-4", "gpt-3.5-turbo"],
            width=300
        )
        self.openai_model.pack(pady=5)
        
        # Gemini Settings
        self.gemini_frame = ctk.CTkFrame(self.ai_tab)
        self.gemini_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            self.gemini_frame,
            text="Gemini Ayarları",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.gemini_key = ctk.CTkEntry(
            self.gemini_frame,
            placeholder_text="Gemini API Key",
            width=300
        )
        self.gemini_key.pack(pady=5)

        self.gemini_model = ctk.CTkComboBox(
            self.gemini_frame,
            values=["gemini-1.5-pro", "gemini-2.0-flash", "gemini-1.5-pro-002", "gemini-1.5-pro-001", "gemini-1.5-flash"],
            width=300
        )
        self.gemini_model.pack(pady=5)



        # Deepseek Settings
        self.deepseek_frame = ctk.CTkFrame(self.ai_tab)
        self.deepseek_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            self.deepseek_frame,
            text="Deepseek Ayarları",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.deepseek_key = ctk.CTkEntry(
            self.deepseek_frame,
            placeholder_text="Deepseek API Key",
            width=300
        )
        self.deepseek_key.pack(pady=5)  # Eklendi

        self.claudeai_frame = ctk.CTkFrame(self.ai_tab)
        self.claudeai_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            self.claudeai_frame,
            text="Claude AI Ayarları",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.claudeai_key = ctk.CTkEntry(
            self.claudeai_frame,
            placeholder_text="Claude AI API Key",
            width=300
        )

        self.claudeai_key.pack(pady=5)  # Eklendi
    
    def _create_appearance_settings(self):
        """Create appearance settings tab content"""
        # Theme Selection
        theme_frame = ctk.CTkFrame(self.appearance_tab)
        theme_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(
            theme_frame,
            text="Tema",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.theme_var = ctk.StringVar(value=self.viewmodel.get_current_theme())
        
        # Light theme option
        light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Açık Tema",
            variable=self.theme_var,
            value="light",
            command=lambda: self.viewmodel.set_theme("light")
        )
        light_radio.pack(pady=5)
        
        # Dark theme option
        dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Koyu Tema",
            variable=self.theme_var,
            value="dark",
            command=lambda: self.viewmodel.set_theme("dark")
        )
        dark_radio.pack(pady=5)
    
    def _create_prompt_settings(self):
        """Create prompt settings tab content"""
        # Prompt Templates
        self.prompt_frame = ctk.CTkScrollableFrame(
            self.prompt_tab,
            width=500,
            height=400
        )
        self.prompt_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add Template Button
        self.add_prompt_btn = ctk.CTkButton(
            self.prompt_tab,
            text="Yeni Şablon Ekle",
            command=self._add_prompt_template
        )
        self.add_prompt_btn.pack(pady=10)
    
    def _create_file_processing_settings(self):
        """Create file processing settings tab"""
        # Main container
        main_frame = ctk.CTkFrame(self.file_processing_tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Otomatik Parçalama Bölümü
        splitting_frame = ctk.CTkFrame(main_frame)
        splitting_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            splitting_frame,
            text="Otomatik Parçalama",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Enable/Disable Switch
        self.auto_split_var = ctk.BooleanVar(value=self.viewmodel.get_setting('auto_split', False))
        auto_split_switch = ctk.CTkSwitch(
            splitting_frame,
            text="Otomatik parçalamayı etkinleştir",
            variable=self.auto_split_var,
            command=self._on_auto_split_changed
        )
        auto_split_switch.pack(anchor="w", padx=20, pady=5)
        
        # Parçalama seçenekleri frame
        self.split_options_frame = ctk.CTkFrame(splitting_frame)
        self.split_options_frame.pack(fill="x", padx=20, pady=10)
        
        # Parça boyutu ayarı
        size_frame = ctk.CTkFrame(self.split_options_frame)
        size_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            size_frame,
            text="Varsayılan parça boyutu (sayfa):",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
        
        self.chunk_size_var = ctk.StringVar(value=str(self.viewmodel.get_setting('chunk_size', 3)))
        chunk_size_entry = ctk.CTkEntry(
            size_frame,
            textvariable=self.chunk_size_var,
            width=100
        )
        chunk_size_entry.pack(side="left", padx=5)
        
        # Dosya boyutu limiti
        limit_frame = ctk.CTkFrame(self.split_options_frame)
        limit_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            limit_frame,
            text="Minimum dosya boyutu (MB):",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
        
        self.min_size_var = ctk.StringVar(value=str(self.viewmodel.get_setting('min_split_size', 1)))
        min_size_entry = ctk.CTkEntry(
            limit_frame,
            textvariable=self.min_size_var,
            width=100
        )
        min_size_entry.pack(side="left", padx=5)
        
        # Birleştirme seçenekleri
        combine_frame = ctk.CTkFrame(main_frame)
        combine_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            combine_frame,
            text="Birleştirme Ayarları",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Birleştirme yöntemi
        method_frame = ctk.CTkFrame(combine_frame)
        method_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            method_frame,
            text="Varsayılan birleştirme yöntemi:",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
        
        self.combine_method_var = ctk.StringVar(value=self.viewmodel.get_setting('combine_method', 'sequential'))
        method_combo = ctk.CTkComboBox(
            method_frame,
            values=["Sıralı Birleştirme", "Özetleyerek Birleştirme"],
            variable=self.combine_method_var,
            width=200
        )
        method_combo.pack(side="left", padx=5)
        
        # İleri Seviye Ayarlar
        advanced_frame = ctk.CTkFrame(main_frame)
        advanced_frame.pack(fill="x")
        
        ctk.CTkLabel(
            advanced_frame,
            text="İleri Seviye Ayarlar",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Paralel işleme
        self.parallel_var = ctk.BooleanVar(value=self.viewmodel.get_setting('parallel_processing', False))
        parallel_switch = ctk.CTkSwitch(
            advanced_frame,
            text="Paralel işlemeyi etkinleştir",
            variable=self.parallel_var
        )
        parallel_switch.pack(anchor="w", padx=20, pady=5)
        
        # Cache ayarı
        self.cache_var = ctk.BooleanVar(value=self.viewmodel.get_setting('enable_cache', True))
        cache_switch = ctk.CTkSwitch(
            advanced_frame,
            text="Sonuçları önbelleğe al",
            variable=self.cache_var
        )
        cache_switch.pack(anchor="w", padx=20, pady=5)
        
        # Initial state update
        self._on_auto_split_changed()
    
    def _add_prompt_template(self):
        """Add new prompt template"""
        template_window = PromptTemplateWindow(self, self.viewmodel)
        template_window.grab_set()
    
    def _save_settings(self):
        """Save all settings"""
        try:
            # Validate number inputs
            try:
                chunk_size = int(self.chunk_size_var.get())
                min_size = float(self.min_size_var.get())
                if chunk_size < 1:
                    raise ValueError("Parça boyutu en az 1 olmalıdır")
                if min_size < 0:
                    raise ValueError("Minimum dosya boyutu 0'dan büyük olmalıdır")
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
                return

            # Collect file processing settings
            file_settings = {
                'auto_split': self.auto_split_var.get(),
                'chunk_size': chunk_size,
                'min_split_size': min_size,
                'combine_method': self.combine_method_var.get(),
                'parallel_processing': self.parallel_var.get(),
                'enable_cache': self.cache_var.get()
            }
            
            # Save settings through viewmodel
            self.viewmodel.save_file_processing_settings(file_settings)
            
            # Save AI settings
            openai_config = {
                'api_key': self.openai_key.get(),
                'model': self.openai_model.get()
            }
            self.viewmodel.save_ai_config('openai', openai_config)
            
            gemini_config = {
                'api_key': self.gemini_key.get()
            }
            self.viewmodel.save_ai_config('gemini', gemini_config)

            deepseek_config = {
            'api_key': self.deepseek_key.get()
            }
            self.viewmodel.save_ai_config('deepseek', deepseek_config)

            claudeai_config = {
                'api_key': self.claudeai_key.get()
            }
            self.viewmodel.save_ai_config('claudeai', claudeai_config)

            
            # Save appearance settings
            ctk.set_appearance_mode(self.theme_var.get())
            
            self.destroy()
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken hata oluştu: {str(e)}")
    
    def _on_auto_split_changed(self):
        """Handle auto split switch change"""
        enabled = self.auto_split_var.get()
        state = "normal" if enabled else "disabled"
        
        # Update UI state
        for child in self.split_options_frame.winfo_children():
            for widget in child.winfo_children():
                try:
                    widget.configure(state=state)
                except:
                    pass
                    
    def _on_settings_saved(self):
        """Handle settings saved event"""
        self._show_success("Başarılı", "Ayarlar başarıyla kaydedildi")
    
    def _show_error(self, message: str):
        """Show error dialog"""
        ctk.CTkMessageBox(
            title="Hata",
            message=message,
            icon="cancel"
        )
    
    def _show_success(self, title: str, message: str):
        """Show success dialog"""
        ctk.CTkMessageBox(
            title=title,
            message=message,
            icon="check"
        )

    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        # Bu eksik:
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def _add_prompt_template(self):
        """Add new prompt template"""
        template_window = PromptTemplateWindow(self, self.viewmodel)  # Bu sınıf eksik
        template_window.grab_set()