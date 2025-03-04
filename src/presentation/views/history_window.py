import customtkinter as ctk
from tkinter import messagebox
import os
from typing import List, Optional, Callable
from src.models.history import AnalysisHistory
from src.repositories.history_repository import HistoryRepository
from src.services.file_processing.result_manager import ProcessingResult
from .result_window import ResultWindow

class HistoryWindow(ctk.CTkToplevel):
    """Window for viewing analysis history"""
    def __init__(self, parent, history_repo: HistoryRepository):
        super().__init__(parent)
        
        self.history_repo = history_repo
        self.current_filter = "all"
        self.current_history: List[AnalysisHistory] = []

        # Pencereyi öne getir
        self.lift()
        self.focus_force()
        
        # Pencere ortada açılsın
        self.center_window()
        
        # Configure window
        self.title("Analiz Geçmişi")
        self.geometry("900x600")
        
        # Create layout
        self._create_layout()
        
        # Load history
        self._load_history()

    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def _create_layout(self):
        """Create window layout"""
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Filter frame
        self._create_filter_frame()
        
        # History list
        self._create_history_list()
    
    def _create_filter_frame(self):
        """Create filter controls"""
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            filter_frame,
            text="Analiz Geçmişi",
            font=("Arial", 18, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Filter combobox
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Filtre:",
            font=("Arial", 12)
        )
        filter_label.pack(side="left", padx=(20, 5))
        
        self.filter_combobox = ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "PDF Dosyaları", "Word Dosyaları", "Excel Dosyaları", "Metin Dosyaları", 
                   "HTML Dosyaları", "CSV Dosyaları", "Resim Dosyaları"],
            width=150,
            command=self._on_filter_changed
        )
        self.filter_combobox.pack(side="left", padx=5)
        
        # Provider filter
        provider_label = ctk.CTkLabel(
            filter_frame,
            text="Sağlayıcı:",
            font=("Arial", 12)
        )
        provider_label.pack(side="left", padx=(20, 5))
        
        self.provider_combobox = ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "OpenAI", "Gemini", "Claude", "DeepSeek"],
            width=100,
            command=self._on_provider_changed
        )
        self.provider_combobox.pack(side="left", padx=5)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            filter_frame,
            text="Yenile",
            width=80,
            command=self._load_history
        )
        self.refresh_button.pack(side="right", padx=10)
    
    def _create_history_list(self):
        """Create history list"""
        # Create scrollable frame
        self.history_frame = ctk.CTkScrollableFrame(self)
        self.history_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # History items will be added here dynamically
    
    def _load_history(self):
        """Load history entries"""
        try:
            # Clear current items
            for widget in self.history_frame.winfo_children():
                widget.destroy()
            
            # Get history based on filter
            if self.current_filter == "all":
                self.current_history = self.history_repo.get_recent_analyses(50)
            else:
                filter_map = {
                    "PDF Dosyaları": ".pdf",
                    "Word Dosyaları": ".docx",
                    "Excel Dosyaları": ".xlsx",
                    "Metin Dosyaları": ".txt",
                    "HTML Dosyaları": ".html",
                    "CSV Dosyaları": ".csv",
                    "Resim Dosyaları": ".png"
                }
                
                if self.current_filter in filter_map:
                    self.current_history = self.history_repo.get_by_file_type(
                        filter_map[self.current_filter], 50)
                else:
                    self.current_history = self.history_repo.get_recent_analyses(50)
            
            # Apply provider filter if needed
            provider = self.provider_combobox.get()
            if provider != "Tümü":
                provider_map = {
                    "OpenAI": "openai",
                    "Gemini": "gemini",
                    "Claude": "claude",
                    "DeepSeek": "deepseek"
                }
                if provider in provider_map:
                    self.current_history = [h for h in self.current_history 
                                         if h.provider == provider_map[provider]]
            
            # Display history entries
            if not self.current_history:
                no_history_label = ctk.CTkLabel(
                    self.history_frame,
                    text="Henüz analiz geçmişi bulunmuyor.",
                    font=("Arial", 14)
                )
                no_history_label.pack(pady=20)
                return
            
            # Add history items
            for i, history in enumerate(self.current_history):
                history_item = HistoryItem(
                    self.history_frame,
                    history=history,
                    on_view=self._view_history_item,
                    on_delete=self._delete_history_item,
                    fg_color="#2f2f2f" if i % 2 == 0 else "#3f3f3f"
                )
                history_item.pack(fill="x", pady=5)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Geçmiş yüklenirken hata oluştu: {str(e)}")

    def _delete_history_item(self, history_id: int):
        """Delete history item"""
        try:
            # Delete from database
            self.history_repo.delete(history_id)
            
            # Refresh the list
            self._load_history()
            
            messagebox.showinfo("Başarılı", "Analiz geçmişi silindi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Analiz geçmişi silinirken hata oluştu: {str(e)}")        
    
    def _on_filter_changed(self, value):
        """Handle filter change"""
        self.current_filter = value if value != "Tümü" else "all"
        self._load_history()
    
    def _on_provider_changed(self, value):
        """Handle provider filter change"""
        self._load_history()
    
    def _view_history_item(self, history_id: int):
        """View history item details"""
        try:
            # Get result from history
            result = self.history_repo.get_result(history_id)
            if result:
                # Show result window
                ResultWindow(self, result)
            else:
                messagebox.showerror("Hata", "Analiz sonucu bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Analiz sonucu görüntülenirken hata oluştu: {str(e)}")

class HistoryItem(ctk.CTkFrame):
    """Single history item widget"""
    def __init__(self, parent, history: AnalysisHistory, on_view: Callable[[int], None], on_delete: Callable[[int], None] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.history = history
        self.on_view = on_view
        self.on_delete = on_delete
        
        self._create_layout()
    
    def _create_layout(self):
        """Create item layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Date and file info
        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        
        date_label = ctk.CTkLabel(
            date_frame,
            text=self.history.formatted_date,
            font=("Arial", 10, "bold")
        )
        date_label.pack(anchor="w")
        
        file_label = ctk.CTkLabel(
            date_frame,
            text=f"{self.history.file_name}",
            font=("Arial", 10)
        )
        file_label.pack(anchor="w")
        
        # Analysis info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nw")
        
        type_label = ctk.CTkLabel(
            info_frame,
            text=f"Analiz: {self.history.analysis_type}",
            font=("Arial", 12, "bold")
        )
        type_label.pack(anchor="w")
        
        provider_label = ctk.CTkLabel(
            info_frame,
            text=f"Sağlayıcı: {self.history.provider}",
            font=("Arial", 10)
        )
        provider_label.pack(anchor="w")
        
        # Summary
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text=self.history.summary,
            font=("Arial", 10),
            justify="left",
            wraplength=800
        )
        summary_label.pack(anchor="w", fill="x")
        
        # View button
        view_button = ctk.CTkButton(
            self,
            text="Görüntüle",
            width=100,
            command=self._on_view_clicked
        )
        view_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

        delete_button = ctk.CTkButton(
            self,
            text="Sil",
            width=100,
            command=self._on_delete_clicked
        )
        delete_button.grid(row=1, column=2, rowspan=2, padx=10, pady=10)
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if messagebox.askyesno("Onay", "Analiz geçmişini silmek istediğinize emin misiniz?"):
            try:
                self.on_delete(self.history.id)
            except Exception as e:
                messagebox.showerror("Hata", f"Analiz geçmişi silinirken hata oluştu: {str(e)}")         

    def _on_view_clicked(self):
        """Handle view button click"""
        if self.on_view:
            self.on_view(self.history.id)