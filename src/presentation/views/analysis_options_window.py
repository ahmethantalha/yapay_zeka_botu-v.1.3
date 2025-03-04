import customtkinter as ctk
from typing import List
import os

class AnalysisOptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent, file_paths: List[str], on_option_selected=None):
        super().__init__(parent)
        
        self.file_paths = file_paths
        self.on_option_selected = on_option_selected
        
        # Configure window
        self.title("Analiz Seçenekleri")
        self.geometry("800x800")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
        
        # Create layout
        self._create_layout()
    
    def _create_layout(self):
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Analiz Seçenekleri",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        # File info
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            file_frame,
            text=f"Seçilen Dosyalar ({len(self.file_paths)}):",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        file_list = ctk.CTkTextbox(
            file_frame,
            height=100,
            font=("Arial", 11)
        )
        file_list.pack(fill="x", padx=10, pady=5)
        
        for file_path in self.file_paths:
            file_list.insert("end", f"• {os.path.basename(file_path)}\n")
        file_list.configure(state="disabled")
        
        # Options frame
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            options_frame,
            text="Analiz Yöntemi:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Analysis options
        self.option_var = ctk.StringVar(value="separate")
        
        # Separate analysis option
        separate_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        separate_frame.pack(fill="x", padx=10, pady=5)
        
        separate_radio = ctk.CTkRadioButton(
            separate_frame,
            text="Her dosyayı ayrı ayrı analiz et",
            variable=self.option_var,
            value="separate",
            font=("Arial", 12)
        )
        separate_radio.pack(side="left")
        
        ctk.CTkLabel(
            separate_frame,
            text="Her dosya için ayrı sonuç penceresi açılır",
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="left", padx=20)
        
        # Combined analysis option
        combine_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        combine_frame.pack(fill="x", padx=10, pady=5)
        
        combine_radio = ctk.CTkRadioButton(
            combine_frame,
            text="Tüm dosyaları birleştirerek analiz et",
            variable=self.option_var,
            value="combine",
            font=("Arial", 12)
        )
        combine_radio.pack(side="left")
        
        ctk.CTkLabel(
            combine_frame,
            text="Tüm dosyalar tek bir metin olarak analiz edilir",
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="left", padx=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="İptal",
            width=100,
            command=self.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Analizi Başlat",
            width=100,
            command=self._start_analysis,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="right", padx=5)
    
    def _start_analysis(self):
        if self.on_option_selected:
            combine_results = self.option_var.get() == "combine"
            self.on_option_selected(self.file_paths, combine_results)
        self.destroy()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))