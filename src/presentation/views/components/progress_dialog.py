import customtkinter as ctk
from tkinter import messagebox
import os
from typing import Optional, Callable

class ProcessProgressDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("İşlem Durumu")
        self.geometry("600x400")
        self.resizable(False, False)
        self.is_cancelled = False

         # Pencereyi önde tut
        self.transient(parent)
        self.grab_set()
        
        self._create_layout()
        self.center_window()
        self.update_idletasks()  # UI'ı güncelleyin
        
    def _create_layout(self):
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="İşlem başlatılıyor...",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=(0, 10))
        
        # Main progress
        self.main_progress = ctk.CTkProgressBar(
            main_frame,
            width=300
        )
        self.main_progress.pack(pady=(0, 20))
        self.main_progress.set(0)
        
        # Current operation frame
        self.current_op_frame = ctk.CTkFrame(main_frame)
        self.current_op_frame.pack(fill="x", pady=(0, 20))
        
        self.current_op_label = ctk.CTkLabel(
            self.current_op_frame,
            text="",
            font=("Arial", 10)
        )
        self.current_op_label.pack(side="left")
        
        # Alt işlem ilerleme çubuğu (eksikti)
        self.current_op_progress = ctk.CTkProgressBar(
            self.current_op_frame,
            width=200
        )
        self.current_op_progress.pack(side="right", padx=10)
        self.current_op_progress.set(0)
        
        # Details text
        self.details_text = ctk.CTkTextbox(
            main_frame,
            height=80,
            font=("Arial", 10)
        )
        self.details_text.pack(fill="x", pady=(0, 10))
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            main_frame,
            text="İptal Et",
            command=self._on_cancel
        )
        self.cancel_button.pack()
        
    def update_progress(self, main_progress: float, operation: str = None, 
                       operation_progress: float = None, details: str = None):
        """Update progress information"""
        self.main_progress.set(main_progress)
        
        if operation:
            self.current_op_label.configure(text=operation)
            if operation_progress is not None:
                self.current_op_progress.set(operation_progress)
        
        if details:
            self.details_text.configure(state="normal")
            self.details_text.insert("end", details + "\n")
            self.details_text.see("end")
            self.details_text.configure(state="disabled")
            
    def _on_cancel(self):
        """Handle cancel button click"""
        if messagebox.askyesno("İptal", "İşlemi iptal etmek istediğinize emin misiniz?"):
            self.is_cancelled = True
            self.status_label.configure(text="İşlem iptal ediliyor...")
            self.cancel_button.configure(state="disabled")
    
    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))