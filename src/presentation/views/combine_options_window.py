import customtkinter as ctk
from src.services.file_processing.result_manager import ProcessingResult, ResultManager
from typing import List

class CombineOptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent, result_count: int, on_option_selected=None):
        super().__init__(parent)
        
        self.result_count = result_count
        self.on_option_selected = on_option_selected
        self.result_manager = ResultManager()
        
        # Configure window
        self.title("Sonuçları Birleştirme Seçenekleri")
        self.geometry("700x700")
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
            text="Sonuçları Birleştirme",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        # Info
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            info_frame,
            text=f"{self.result_count} adet analiz sonucunu nasıl birleştirmek istediğinizi seçin:",
            font=("Arial", 12)
        ).pack(padx=10, pady=10)
        
        # Options frame
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        # Combination types
        self.combination_var = ctk.StringVar(value="sequential")
        
        for combo_type in self.result_manager.get_combination_types():
            option_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
            option_frame.pack(fill="x", padx=10, pady=10)
            
            radio = ctk.CTkRadioButton(
                option_frame,
                text=combo_type["name"],
                variable=self.combination_var,
                value=combo_type["id"],
                font=("Arial", 12)
            )
            radio.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(
                option_frame,
                text=combo_type["description"],
                font=("Arial", 10),
                text_color="gray",
                wraplength=500
            )
            desc_label.pack(pady=(5, 0), padx=25)
        
        # Preview frame (placeholder for future feature)
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            preview_frame,
            text="Önizleme",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        preview_text = ctk.CTkTextbox(
            preview_frame,
            height=100,
            font=("Arial", 11)
        )
        preview_text.pack(fill="x", padx=10, pady=5)
        preview_text.insert("1.0", "Seçilen birleştirme yöntemine göre sonuç formatı...")
        preview_text.configure(state="disabled")
        
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
            text="Birleştir",
            width=100,
            command=self._combine_results,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="right", padx=5)
    
    def _combine_results(self):
        if self.on_option_selected:
            self.on_option_selected(self.combination_var.get())
        self.destroy()

    def _combine_and_show_results(self, results: List[ProcessingResult], combination_type: str):
        """Combine results and show"""
        try:
            # İlerleme bildirimi
            self.update_progress_text(f"Sonuçlar birleştiriliyor ({combination_type})...")
            
            combined = self.result_manager.combine_results(results, combination_type)
            
            # İlerleme bildirimi
            self.update_progress_text("Birleştirme tamamlandı. Sonuçlar gösteriliyor...")
            
            self._show_results(combined)
        except Exception as e:
            self._show_error(f"Sonuçlar birleştirilirken hata oluştu: {str(e)}")
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))