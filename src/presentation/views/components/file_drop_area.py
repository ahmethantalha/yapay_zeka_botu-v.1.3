# src/presentation/views/components/file_drop_area.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os

class FileDropArea(ctk.CTkFrame):
    def __init__(self, master, on_file_drop):
        super().__init__(master)
        
        self.on_file_drop = on_file_drop
        
        # Configure drop area
        self.configure(fg_color="#3b3b3b")
        
        # Minimum yükseklik
        self.configure(height=100)
        
        # Responsive layout grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Labels container
        self.labels_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.labels_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create label
        self.label = ctk.CTkLabel(
            self.labels_frame,
            text="Dosyaları buraya sürükleyin\nveya tıklayarak seçin",
            font=("Arial", 14)
        )
        self.label.pack(anchor="center")
        
        # Create file types label
        self.file_types_label = ctk.CTkLabel(
            self.labels_frame,
            text="Desteklenen formatlar: mp3, wav,m4a, flac, PDF, DOCX, TXT, XLSX, CSV, HTML, XML, EPUB, PNG, JPG",
            font=("Arial", 9)
        )
        self.file_types_label.pack(anchor="center", pady=(5, 0))
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event):
        """Handle click event to open file dialog"""
        # Standart tkinter'dan dosya diyaloğunu kullan
        file_paths = filedialog.askopenfilenames(
            filetypes=[
                ("Tüm Dosyalar", "*.*"),
                ("PDF Dosyaları", "*.pdf"),
                ("Word Dosyaları", "*.docx"),
                ("Excel Dosyaları", "*.xlsx;*.xls"),
                ("Metin Dosyaları", "*.txt"),
                ("CSV Dosyaları", "*.csv"),
                ("Web Dosyaları", "*.html;*.htm;*.xml"),
                ("E-Kitap", "*.epub"),
                ("JSON Dosyaları", "*.json"),
                ("Resim Dosyaları", "*.png;*.jpg;*.jpeg"),
                ("Ses Dosyaları", "*.mp3;*.wav;*.m4a;*.flac")
            ]
        )
        
        if file_paths:  # Bir veya daha fazla dosya seçildiyse
            # Dosya yollarını listeye dönüştür
            file_paths_list = list(file_paths)
            self.on_file_drop(file_paths_list)