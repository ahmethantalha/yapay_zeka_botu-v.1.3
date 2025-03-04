import customtkinter as ctk
from tkinter import messagebox

class PromptTemplateWindow(ctk.CTkToplevel):
    def __init__(self, parent, viewmodel):
        super().__init__(parent)
        
        self.viewmodel = viewmodel
        
        self.title("Yeni Prompt Şablonu")
        self.geometry("500x400")
        
        # Center window
        self.center_window()
        
        # Template Name
        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Şablon Adı",
            width=300
        )
        self.name_entry.pack(pady=10)
        
        # Template Description
        self.desc_label = ctk.CTkLabel(self, text="Açıklama")
        self.desc_label.pack(pady=(10, 0))
        
        self.desc_entry = ctk.CTkTextbox(
            self,
            width=300,
            height=100
        )
        self.desc_entry.pack(pady=5)
        
        # Template Text
        self.template_label = ctk.CTkLabel(self, text="Şablon Metni")
        self.template_label.pack(pady=(10, 0))
        
        self.template_text = ctk.CTkTextbox(
            self,
            width=300,
            height=150
        )
        self.template_text.pack(pady=5)
        
        # Save Button
        self.save_btn = ctk.CTkButton(
            self,
            text="Şablonu Kaydet",
            command=self._save_template
        )
        self.save_btn.pack(pady=10)
    
    def _save_template(self):
        """Save prompt template"""
        user_id = 1  # Default user ID
        name = self.name_entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        template_text = self.template_text.get("1.0", "end-1c")
        
        if not name or not template_text:
            self._show_error("Şablon adı ve metni gereklidir")
            return
        
        self.viewmodel.save_prompt_template(user_id, name, description, template_text)
        self.destroy()
    
    def _show_error(self, message: str):
        """Show error dialog"""
        messagebox.showerror("Hata", message)

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))