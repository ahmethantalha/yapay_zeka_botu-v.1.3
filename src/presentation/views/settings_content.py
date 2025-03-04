# src/presentation/views/settings_content.py
import customtkinter as ctk
from tkinter import messagebox
import os
import json

class SimplifiedSettingsContent(ctk.CTkFrame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        
        self.main_window = main_window
        
        # Model seçenekleri
        self.openai_models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-instruct"]
        self.gemini_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-1.0-pro-vision"]
        self.claude_models = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-2.1", "claude-2.0"]
        self.deepseek_models = ["deepseek-chat", "deepseek-coder"]
        
        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create layout
        self._create_layout()
        
        # Load existing settings
        self._load_settings()
    
    def _create_section_header(self, text):
        """Create section header"""
        header = ctk.CTkLabel(
            self.scrollable_frame,
            text=text,
            font=("Arial", 16, "bold")
        )
        header.pack(anchor="w", pady=(20, 5), padx=10)
    
    def _create_layout(self):
        """Create settings layout"""
        # OpenAI Settings
        self._create_section_header("OpenAI Ayarları")
        
        self.openai_frame = ctk.CTkFrame(self.scrollable_frame)
        self.openai_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.openai_frame,
            text="API Anahtarı:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.openai_key = ctk.CTkEntry(
            self.openai_frame,
            placeholder_text="OpenAI API Key",
            width=400
        )
        self.openai_key.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            self.openai_frame,
            text="Model:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.openai_model_var = ctk.StringVar(value=self.openai_models[0])
        self.openai_model = ctk.CTkComboBox(
            self.openai_frame,
            values=self.openai_models,
            variable=self.openai_model_var,
            width=400
        )
        self.openai_model.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Gemini Settings
        self._create_section_header("Gemini Ayarları")
        
        self.gemini_frame = ctk.CTkFrame(self.scrollable_frame)
        self.gemini_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.gemini_frame,
            text="API Anahtarı:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.gemini_key = ctk.CTkEntry(
            self.gemini_frame,
            placeholder_text="Gemini API Key",
            width=400
        )
        self.gemini_key.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            self.gemini_frame,
            text="Model:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.gemini_model_var = ctk.StringVar(value=self.gemini_models[0])
        self.gemini_model = ctk.CTkComboBox(
            self.gemini_frame,
            values=self.gemini_models,
            variable=self.gemini_model_var,
            width=400
        )
        self.gemini_model.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Claude Settings
        self._create_section_header("Claude Ayarları")
        
        self.claude_frame = ctk.CTkFrame(self.scrollable_frame)
        self.claude_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.claude_frame,
            text="API Anahtarı:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.claude_key = ctk.CTkEntry(
            self.claude_frame,
            placeholder_text="Claude API Key",
            width=400
        )
        self.claude_key.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            self.claude_frame,
            text="Model:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.claude_model_var = ctk.StringVar(value=self.claude_models[0])
        self.claude_model = ctk.CTkComboBox(
            self.claude_frame,
            values=self.claude_models,
            variable=self.claude_model_var,
            width=400
        )
        self.claude_model.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # DeepSeek Settings
        self._create_section_header("DeepSeek Ayarları")
        
        self.deepseek_frame = ctk.CTkFrame(self.scrollable_frame)
        self.deepseek_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.deepseek_frame,
            text="API Anahtarı:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.deepseek_key = ctk.CTkEntry(
            self.deepseek_frame,
            placeholder_text="DeepSeek API Key",
            width=400
        )
        self.deepseek_key.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            self.deepseek_frame,
            text="Model:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.deepseek_model_var = ctk.StringVar(value=self.deepseek_models[0])
        self.deepseek_model = ctk.CTkComboBox(
            self.deepseek_frame,
            values=self.deepseek_models,
            variable=self.deepseek_model_var,
            width=400
        )
        self.deepseek_model.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Genel Ayarlar
        self._create_section_header("Genel Ayarlar")
        
        self.general_frame = ctk.CTkFrame(self.scrollable_frame)
        self.general_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.general_frame,
            text="Varsayılan AI Modeli:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.default_ai_var = ctk.StringVar(value="OpenAI")
        self.default_ai = ctk.CTkComboBox(
            self.general_frame,
            values=["OpenAI", "Gemini", "Claude", "DeepSeek"],
            variable=self.default_ai_var,
            width=400
        )
        self.default_ai.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Ayarları Kaydet",
            font=("Arial", 14, "bold"),
            command=self._save_settings,
            height=40
        )
        self.save_button.pack(pady=20)
    
    def _load_settings(self):
        """Load existing API keys and models"""
        try:
            # Eski tarzdaki ayarları yükle
            openai_key = os.getenv("OPENAI_API_KEY", "")
            gemini_key = os.getenv("GEMINI_API_KEY", "")
            claude_key = os.getenv("CLAUDE_API_KEY", "")
            deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
            
            # Ayarlar dosyasını kontrol et
            settings_file = os.path.join(os.path.dirname(__file__), "../../../data/settings.json")
            
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Model ayarları
                if "openai" in settings:
                    if "model" in settings["openai"] and settings["openai"]["model"] in self.openai_models:
                        self.openai_model_var.set(settings["openai"]["model"])
                
                if "gemini" in settings:
                    if "model" in settings["gemini"] and settings["gemini"]["model"] in self.gemini_models:
                        self.gemini_model_var.set(settings["gemini"]["model"])
                
                if "claude" in settings:
                    if "model" in settings["claude"] and settings["claude"]["model"] in self.claude_models:
                        self.claude_model_var.set(settings["claude"]["model"])
                
                if "deepseek" in settings:
                    if "model" in settings["deepseek"] and settings["deepseek"]["model"] in self.deepseek_models:
                        self.deepseek_model_var.set(settings["deepseek"]["model"])
                
                # Varsayılan AI
                if "default_ai" in settings and settings["default_ai"] in ["OpenAI", "Gemini", "Claude", "DeepSeek"]:
                    self.default_ai_var.set(settings["default_ai"])
            
            # API anahtarlarını ayarla
            if openai_key:
                self.openai_key.insert(0, openai_key)
            
            if gemini_key:
                self.gemini_key.insert(0, gemini_key)
            
            if claude_key:
                self.claude_key.insert(0, claude_key)
            
            if deepseek_key:
                self.deepseek_key.insert(0, deepseek_key)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar yüklenirken hata oluştu: {str(e)}")
    
    def _save_settings(self):
        """Save API keys and models to settings file"""
        try:
            # API anahtarları
            openai_key = self.openai_key.get()
            gemini_key = self.gemini_key.get()
            claude_key = self.claude_key.get()
            deepseek_key = self.deepseek_key.get()
            
            # Model seçimleri
            openai_model = self.openai_model_var.get()
            gemini_model = self.gemini_model_var.get()
            claude_model = self.claude_model_var.get()
            deepseek_model = self.deepseek_model_var.get()
            
            # Varsayılan AI
            default_ai = self.default_ai_var.get()
            
            # Update environment variables
            os.environ["OPENAI_API_KEY"] = openai_key
            os.environ["GEMINI_API_KEY"] = gemini_key
            os.environ["CLAUDE_API_KEY"] = claude_key
            os.environ["DEEPSEEK_API_KEY"] = deepseek_key
            
            # Write to .env file
            with open(".env", "w", encoding='utf-8') as f:
                f.write(f"OPENAI_API_KEY={openai_key}\n")
                f.write(f"GEMINI_API_KEY={gemini_key}\n")
                f.write(f"CLAUDE_API_KEY={claude_key}\n")
                f.write(f"DEEPSEEK_API_KEY={deepseek_key}\n")
                f.write("DATABASE_URL=sqlite:///app.db\n")
            
            # Ayarlar dizinini kontrol et
            settings_dir = os.path.join(os.path.dirname(__file__), "../../../data")
            os.makedirs(settings_dir, exist_ok=True)
            
            # Write to settings.json
            settings = {
                "openai": {
                    "model": openai_model
                },
                "gemini": {
                    "model": gemini_model
                },
                "claude": {
                    "model": claude_model
                },
                "deepseek": {
                    "model": deepseek_model
                },
                "default_ai": default_ai
            }
            
            settings_file = os.path.join(settings_dir, "settings.json")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Başarılı", "Ayarlar başarıyla kaydedildi")
            
            # Uygulamayı yeniden başlatmak için öner
            restart = messagebox.askyesno("Yeniden Başlat", 
                                        "Değişikliklerin etkili olması için uygulamayı yeniden başlatmak gerekiyor. Şimdi yeniden başlatmak ister misiniz?")
            if restart:
                self.main_window.destroy()
                import sys
                os.execl(sys.executable, sys.executable, *sys.argv)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken hata oluştu: {str(e)}")