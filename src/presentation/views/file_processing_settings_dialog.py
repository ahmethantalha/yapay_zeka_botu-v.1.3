# src/presentation/views/file_processing_settings_dialog.py
import customtkinter as ctk
from tkinter import messagebox

class FileProcessingSettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, current_settings=None):
        super().__init__(parent)
        
        self.result = None  # Dialog sonucu
        self.current_settings = current_settings or {
            'auto_split': False,
            'chunk_size': 3
        }
        
        # Pencere ayarları
        self.title("Dosya Parçalama Ayarları")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Modal pencere yap
        self.transient(parent)
        self.grab_set()
        
        # Layout oluştur
        self._create_layout()
        self.center_window()
    
    def _create_layout(self):
        # Ana frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Otomatik parçalama switch'i
        self.auto_split_var = ctk.BooleanVar(value=self.current_settings['auto_split'])
        auto_split_switch = ctk.CTkSwitch(
            main_frame,
            text="Otomatik Parçalama",
            variable=self.auto_split_var,
            command=self._on_auto_split_changed
        )
        auto_split_switch.pack(anchor="w", pady=(0, 5))
        
        # Parça boyutu ayarı
        self.chunk_frame = ctk.CTkFrame(main_frame)
        self.chunk_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            self.chunk_frame,
            text="Her parçanın sayfa sayısı:"
        ).pack(side="left", padx=5)
        
        self.chunk_size_var = ctk.StringVar(value=str(self.current_settings['chunk_size']))
        chunk_size_entry = ctk.CTkEntry(
            self.chunk_frame,
            textvariable=self.chunk_size_var,
            width=50
        )
        chunk_size_entry.pack(side="left", padx=5)
        
        # Bilgi metni
        info_text = """
        Dosya parçalama, büyük dosyaları daha küçük parçalara bölerek
        daha etkili analiz yapılmasını sağlar.
        
        Daha detaylı ayarlar için Ayarlar penceresini kullanabilirsiniz.
        """
        
        self.info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=("Arial", 10),
            text_color="gray",
            wraplength=350
        )
        self.info_label.pack(pady=20)
        
        # Butonlar
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            button_frame,
            text="İptal",
            width=100,
            command=self.destroy
        ).pack(side="left")
        
        ctk.CTkButton(
            button_frame,
            text="Kaydet",
            width=100,
            command=self._save_settings
        ).pack(side="right")
        
        # Başlangıç durumunu güncelle
        self._update_settings_state()
    
    def _on_auto_split_changed(self):
        """Handle auto split switch change"""
        self._update_settings_state()
    
    def _update_settings_state(self):
        """Update UI state based on auto split setting"""
        enabled = self.auto_split_var.get()
        for child in self.chunk_frame.winfo_children():
            child.configure(state="normal" if enabled else "disabled")
    
    def _save_settings(self):
        """Save settings and close dialog"""
        try:
            chunk_size = int(self.chunk_size_var.get())
            if chunk_size < 1:
                raise ValueError("Parça boyutu en az 1 olmalıdır")
                
            self.result = {
                'auto_split': self.auto_split_var.get(),
                'chunk_size': chunk_size
            }
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))