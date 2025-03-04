import customtkinter as ctk
import os

class FileSplittingWindow(ctk.CTkToplevel):
    def __init__(self, parent, file_path: str, on_split_selected=None):
        super().__init__(parent)
        
        self.file_path = file_path
        self.on_split_selected = on_split_selected
        
        # Configure window
        self.title("Dosya Bölme Seçenekleri")
        self.geometry("900x900")
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
            text="Dosya Bölme Seçenekleri",
            font=("Arial", 20, "bold")
        ).pack(side="left")
        
        # File info
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        file_size = os.path.getsize(self.file_path) / (1024 * 1024)  # MB cinsinden
        
        ctk.CTkLabel(
            file_frame,
            text=f"Dosya: {os.path.basename(self.file_path)}",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            file_frame,
            text=f"Boyut: {file_size:.2f} MB",
            font=("Arial", 11)
        ).pack(anchor="w", padx=10, pady=5)
        
        # Splitting options
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        # Method selection
        method_frame = ctk.CTkFrame(options_frame)
        method_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            method_frame,
            text="Bölme Yöntemi:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=5)
        
        self.method_var = ctk.StringVar(value="page")
        
        methods = [
            ("Sayfa Bazlı", "page", "Belgeyi sayfa sayısına göre böler"),
            ("Token Bazlı", "token", "Belgeyi kelime sayısına göre böler (AI modeli için optimize)")
        ]
        
        for name, value, desc in methods:
            method_option = ctk.CTkFrame(method_frame, fg_color="transparent")
            method_option.pack(fill="x", pady=5)
            
            radio = ctk.CTkRadioButton(
                method_option,
                text=name,
                variable=self.method_var,
                value=value,
                font=("Arial", 12)
            )
            radio.pack(side="left")
            
            ctk.CTkLabel(
                method_option,
                text=desc,
                font=("Arial", 10),
                text_color="gray"
            ).pack(side="left", padx=20)
        
        # Size settings
        size_frame = ctk.CTkFrame(options_frame)
        size_frame.pack(fill="x", padx=10, pady=10)
        
        # Page size frame
        self.page_size_frame = ctk.CTkFrame(size_frame)
        self.page_size_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            self.page_size_frame,
            text="Her parçadaki sayfa sayısı:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=5)
        
        size_control_frame = ctk.CTkFrame(self.page_size_frame, fg_color="transparent")
        size_control_frame.pack(fill="x")
        
        self.size_slider = ctk.CTkSlider(
            size_control_frame,
            from_=1,
            to=50,
            number_of_steps=49,
            command=self._update_size_label
        )
        self.size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.size_slider.set(10)
        
        self.size_label = ctk.CTkLabel(
            size_control_frame,
            text="10 sayfa",
            font=("Arial", 12)
        )
        self.size_label.pack(side="right", padx=5)
        
        # Estimated parts info
        self.parts_label = ctk.CTkLabel(
            self.page_size_frame,
            text="Tahmini parça sayısı: Hesaplanıyor...",
            font=("Arial", 10),
            text_color="gray"
        )
        self.parts_label.pack(anchor="w", pady=5)
        
        # Additional options
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            options_frame,
            text="İşlem Seçenekleri:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Combine results option
        self.combine_var = ctk.BooleanVar(value=True)
        combine_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        combine_frame.pack(fill="x", padx=10, pady=5)
        
        combine_check = ctk.CTkCheckBox(
            combine_frame,
            text="Analiz sonuçlarını birleştir",
            variable=self.combine_var,
            font=("Arial", 12)
        )
        combine_check.pack(side="left")
        
        ctk.CTkLabel(
            combine_frame,
            text="Tüm parçaların analiz sonuçları tek bir raporda birleştirilir",
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="left", padx=20)
        
        # Preview frame
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            preview_frame,
            text="Bölme Önizleme",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            height=100,
            font=("Arial", 11)
        )
        self.preview_text.pack(fill="x", padx=10, pady=5)
        
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
            command=self._start_splitting,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="right", padx=5)
        
        # Initial updates
        self._update_size_label(self.size_slider.get())
        self._update_preview()
        
        # Bind method change
        self.method_var.trace_add("write", lambda *args: self._update_preview())
    
    def _update_size_label(self, value):
        """Update size label and estimated parts"""
        page_count = int(value)
        self.size_label.configure(text=f"{page_count} sayfa")
        
        try:
            total_pages = self._get_total_pages()
            est_parts = (total_pages + page_count - 1) // page_count  # Round up division
            self.parts_label.configure(text=f"Tahmini parça sayısı: {est_parts}")
        except:
            self.parts_label.configure(text="Tahmini parça sayısı: Hesaplanamadı")
        
        self._update_preview()
    
    def _get_total_pages(self):
        """Get total pages in document"""
        # This is a placeholder. Actual implementation would depend on file type
        return 100  # Example value
    
    def _update_preview(self):
        """Update preview text"""
        method = self.method_var.get()
        size = int(self.size_slider.get())
        
        preview = "Bölme Özeti:\n\n"
        
        if method == "page":
            preview += f"• Dosya sayfa bazlı bölünecek\n"
            preview += f"• Her parça maksimum {size} sayfa içerecek\n"
        else:
            preview += f"• Dosya token bazlı bölünecek\n"
            preview += f"• Her parça yaklaşık {size * 500} kelime içerecek\n"
        
        if self.combine_var.get():
            preview += "\nTüm parçaların analiz sonuçları otomatik olarak birleştirilecek"
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", preview)
        self.preview_text.configure(state="disabled")
    
    def _start_splitting(self):
        """Start splitting process"""
        if self.on_split_selected:
            options = {
                'chunk_size': int(self.size_slider.get()),
                'method': self.method_var.get(),
                'combine_results': self.combine_var.get()
            }
            self.on_split_selected(self.file_path, options)
        self.destroy()
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))