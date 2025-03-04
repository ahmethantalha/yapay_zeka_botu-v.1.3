import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, fg_color="#333333", **kwargs)
        
        # Responsive grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Hazır",
            font=("Arial", 10)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=2, sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            width=100
        )
        self.progress_bar.grid(row=0, column=1, padx=10, pady=2, sticky="e")
        self.progress_bar.set(0)  # Başlangıçta gizli
        self.progress_bar.grid_remove()  # Başlangıçta gizli
    
    def set_status(self, text: str):
        """Update status text"""
        self.status_label.configure(text=text)
    
    def start_progress(self):
        """Start progress bar animation"""
        self.progress_bar.grid()  # Göster
        self.progress_bar.start()
    
    def stop_progress(self):
        """Stop progress bar animation"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()  # Gizle
