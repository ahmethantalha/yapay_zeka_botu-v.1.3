import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from src.services.file_processing.result_manager import ProcessingResult, ResultManager

class ResultWindow(ctk.CTkToplevel):
    def __init__(self, parent, result: ProcessingResult):
        super().__init__(parent)
        
        self.result = result
        self.result_manager = ResultManager()
        # Pencereyi öne getir
        self.lift()
        self.focus_force()
        
        # Pencere ortada açılsın
        self.center_window()

        # Configure window
        self.title("Analiz Sonuçları")
        self.geometry("900x600")

        self._create_layout()
    
    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def _create_layout(self):
        """Create the results window layout"""
        # Create main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create metadata frame
        self._create_metadata_frame()
        
        # Create text display
        self._create_text_display()
        
        # Create export frame
        self._create_export_frame()
    
    def _create_metadata_frame(self):
        """Create frame for metadata display"""
        metadata_frame = ctk.CTkFrame(self)
        metadata_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # File info
        ctk.CTkLabel(
            metadata_frame,
            text=f"Dosya: {self.result.file_name}",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=10)
        
        # Analysis type
        ctk.CTkLabel(
            metadata_frame,
            text=f"Analiz: {self.result.analysis_type}",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
        
        # Timestamp
        ctk.CTkLabel(
            metadata_frame,
            text=f"Tarih: {self.result.timestamp.strftime('%Y-%m-%d %H:%M')}",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
    
    def _create_text_display(self):
        """Create text display area"""
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Original text tab
        original_tab = self.notebook.add("Orijinal Metin")
        self.original_text = ctk.CTkTextbox(
            original_tab,
            wrap="word",
            font=("Arial", 12)
        )
        self.original_text.pack(fill="both", expand=True)
        self.original_text.insert("1.0", self.result.original_text)
        self.original_text.configure(state="disabled")
        
        # Analysis tab
        analysis_tab = self.notebook.add("Analiz")
        self.analysis_text = ctk.CTkTextbox(
            analysis_tab,
            wrap="word",
            font=("Arial", 12)
        )
        self.analysis_text.pack(fill="both", expand=True)
        self.analysis_text.insert("1.0", self.result.analyzed_text)
        self.analysis_text.configure(state="disabled")
    
    def _create_export_frame(self):
        """Create frame for export options"""
        export_frame = ctk.CTkFrame(self)
        export_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Export format selection
        self.format_var = ctk.StringVar(value="pdf")
        
        ctk.CTkLabel(
            export_frame,
            text="Dışa Aktarma Formatı:",
            font=("Arial", 12)
        ).pack(side="left", padx=10)
        
        for format in ["PDF", "DOCX", "TXT", "JSON", "MD"]:
            ctk.CTkRadioButton(
                export_frame,
                text=format,
                variable=self.format_var,
                value=format.lower()
            ).pack(side="left", padx=10)
        
        # Export button
        ctk.CTkButton(
            export_frame,
            text="Dışa Aktar",
            command=self._export_result
        ).pack(side="right", padx=10)
    
    def _export_result(self):
        """Export result in selected format"""
        format = self.format_var.get()
        
        file_types = {
            'pdf': ('PDF dosyaları', '*.pdf'),
            'docx': ('Word dosyaları', '*.docx'),
            'txt': ('Metin dosyaları', '*.txt'),
            'json': ('JSON dosyaları', '*.json'),
            'md': ('Markdown dosyaları', '*.md')
        }
        
        output_path = filedialog.asksaveasfilename(
            defaultextension=f".{format}",
            filetypes=[file_types[format]]
        )
        
        if output_path:
            try:
                self.result_manager.save_result(
                    self.result,
                    format,
                    output_path
                )
                
                self._show_success("Dışa Aktarma Başarılı", 
                    f"Sonuçlar {os.path.basename(output_path)} dosyasına aktarıldı")
                
            except Exception as e:
                self._show_error("Dışa Aktarma Başarısız", str(e))
    
    def _show_success(self, title: str, message: str):
        """Show success dialog"""
        messagebox.showinfo(title, message)
    
    def _show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)

    