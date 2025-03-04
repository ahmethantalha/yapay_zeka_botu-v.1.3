# src/presentation/views/prompt_manager_window.py (YENİ DOSYA)

import customtkinter as ctk
from tkinter import messagebox
import os
import json
from typing import List, Dict, Any, Optional

class PromptTemplateItem(ctk.CTkFrame):
    """Tek bir şablon için UI öğesi"""
    def __init__(self, parent, name: str, description: str, template_text: str, 
                 on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.name = name
        self.description = description
        self.template_text = template_text
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._create_layout()
    
    def _create_layout(self):
        """Create item layout"""
        # Name label
        self.name_label = ctk.CTkLabel(
            self,
            text=self.name,
            font=("Arial", 14, "bold")
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        # Description label
        self.desc_label = ctk.CTkLabel(
            self,
            text=self.description,
            font=("Arial", 10),
            wraplength=400
        )
        self.desc_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="e")
        
        # Edit button
        self.edit_button = ctk.CTkButton(
            self.buttons_frame,
            text="Düzenle",
            width=80,
            command=self._handle_edit
        )
        self.edit_button.pack(side="left", padx=5)
        
        # Delete button
        self.delete_button = ctk.CTkButton(
            self.buttons_frame,
            text="Sil",
            width=80,
            fg_color="#dc3545",  # Kırmızı
            hover_color="#c82333",  # Koyu kırmızı
            command=self._handle_delete
        )
        self.delete_button.pack(side="left", padx=5)
    
    def _handle_edit(self):
        """Handle edit button click"""
        if self.on_edit:
            self.on_edit(self.name, self.description, self.template_text)
    
    def _handle_delete(self):
        """Handle delete button click"""
        if self.on_delete:
            self.on_delete(self.name)

class PromptManagerWindow(ctk.CTkToplevel):
    """Prompt şablonları yönetim penceresi"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure window
        self.title("Şablon Yöneticisi")
        self.geometry("700x600")
        
        # Şablonları saklayacak değişken
        self.templates: List[Dict[str, Any]] = []
        
        # Dosya yolunu belirle
        self.templates_file = os.path.join(os.path.dirname(__file__), "../../../data/templates.json")
        os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
        
        # Create layout
        self._create_layout()
        
        # Load templates
        self._load_templates()
    
    def _create_layout(self):
        """Create window layout"""
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header frame
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Prompt Şablonları",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(side="left")
        
        # Add button
        self.add_button = ctk.CTkButton(
            self.header_frame,
            text="Yeni Şablon Ekle",
            command=self._show_add_template_dialog
        )
        self.add_button.pack(side="right")
        
        # Templates list frame
        self.templates_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.templates_frame.pack(fill="both", expand=True)
    
    def _load_templates(self):
        """Load templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                # Create with default templates
                self.templates = [
                    {
                        "name": "Genel Özet",
                        "description": "Verilen metni kapsamlı bir şekilde özetler",
                        "template_text": "Aşağıdaki metni kapsamlı bir şekilde özetleyin.\n\nÖzet yazarken dikkat edilecek noktalar:\n- Ana fikirleri koruyun\n- Gereksiz detayları çıkarın\n- Kronolojik sırayı koruyun\n- Profesyonel bir dil kullanın"
                    },
                    {
                        "name": "Teknik Analiz",
                        "description": "Teknik içerikli metinleri analiz eder",
                        "template_text": "Metni teknik açıdan analiz edin.\n\nRapor Yapısı:\n1. Teknik Özet\n2. Kullanılan Teknolojiler\n3. Teknik Terimler Sözlüğü\n4. Uygulama Adımları\n5. Teknik Gereksinimler\n6. Potansiyel Sorunlar ve Çözüm Önerileri"
                    }
                ]
                self._save_templates()
            
            # Display templates
            self._populate_templates_list()
        except Exception as e:
            messagebox.showerror("Hata", f"Şablonlar yüklenemedi: {str(e)}")
    
    def _save_templates(self):
        """Save templates to file"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Hata", f"Şablonlar kaydedilemedi: {str(e)}")
    
    def _populate_templates_list(self):
        """Display templates in the list"""
        # Clear current items
        for widget in self.templates_frame.winfo_children():
            widget.destroy()
        
        # No templates message
        if not self.templates:
            no_templates_label = ctk.CTkLabel(
                self.templates_frame,
                text="Henüz şablon bulunmuyor. Yeni bir şablon ekleyin.",
                font=("Arial", 12),
                fg_color="transparent"
            )
            no_templates_label.pack(pady=20)
            return
        
        # Add template items
        for i, template in enumerate(self.templates):
            template_item = PromptTemplateItem(
                self.templates_frame,
                name=template["name"],
                description=template["description"],
                template_text=template["template_text"],
                on_edit=self._handle_edit_template,
                on_delete=self._handle_delete_template,
                fg_color="#2f2f2f" if i % 2 == 0 else "#3f3f3f"
            )
            template_item.pack(fill="x", pady=5)
    
    def _show_add_template_dialog(self):
        """Show dialog to add new template"""
        self._show_template_dialog()
    
    def _handle_edit_template(self, name: str, description: str, template_text: str):
        """Handle template edit"""
        self._show_template_dialog(name, description, template_text)
    
    def _handle_delete_template(self, name: str):
        """Handle template delete"""
        confirm = messagebox.askyesno("Onay", f"'{name}' şablonunu silmek istediğinizden emin misiniz?")
        if confirm:
            # Remove template
            self.templates = [t for t in self.templates if t["name"] != name]
            
            # Save and refresh
            self._save_templates()
            self._populate_templates_list()
    
    def _show_template_dialog(self, name: str = "", description: str = "", template_text: str = ""):
        """Show dialog to add/edit template"""
        dialog = TemplateDialog(self, name, description, template_text)
        self.wait_window(dialog)
        
        if dialog.result:
            new_name, new_description, new_template_text = dialog.result
            
            # Check if editing existing template
            if name:
                # Update existing template
                for template in self.templates:
                    if template["name"] == name:
                        template["name"] = new_name
                        template["description"] = new_description
                        template["template_text"] = new_template_text
                        break
            else:
                # Add new template
                self.templates.append({
                    "name": new_name,
                    "description": new_description,
                    "template_text": new_template_text
                })
            
            # Save and refresh
            self._save_templates()
            self._populate_templates_list()

class TemplateDialog(ctk.CTkToplevel):
    """Dialog for adding/editing templates"""
    def __init__(self, parent, name: str = "", description: str = "", template_text: str = ""):
        super().__init__(parent)
        
        # Configure dialog
        self.title("Şablon " + ("Düzenle" if name else "Ekle"))
        self.geometry("600x500")
        self.resizable(True, True)
        
        # Initial values
        self.name = name
        self.description = description
        self.template_text = template_text
        
        # Result
        self.result = None
        
        # Create layout
        self._create_layout()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
    
    def _create_layout(self):
        """Create dialog layout"""
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="Şablon Adı:",
            font=("Arial", 12, "bold")
        )
        self.name_label.pack(anchor="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            width=560
        )
        self.name_entry.pack(fill="x", pady=(0, 10))
        if self.name:
            self.name_entry.insert(0, self.name)
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Açıklama:",
            font=("Arial", 12, "bold")
        )
        self.desc_label.pack(anchor="w", pady=(0, 5))
        
        self.desc_entry = ctk.CTkEntry(
            self.main_frame,
            width=560
        )
        self.desc_entry.pack(fill="x", pady=(0, 10))
        if self.description:
            self.desc_entry.insert(0, self.description)
        
        # Template text
        self.text_label = ctk.CTkLabel(
            self.main_frame,
            text="Şablon Metni:",
            font=("Arial", 12, "bold")
        )
        self.text_label.pack(anchor="w", pady=(0, 5))
        
        self.text_entry = ctk.CTkTextbox(
            self.main_frame,
            width=560,
            height=250
        )
        self.text_entry.pack(fill="both", expand=True, pady=(0, 10))
        if self.template_text:
            self.text_entry.insert("1.0", self.template_text)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="İptal",
            width=100,
            command=self.destroy
        )
        self.cancel_button.pack(side="left", padx=5)
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Kaydet",
            width=100,
            command=self._save
        )
        self.save_button.pack(side="right", padx=5)
    
    def _save(self):
        """Save template and close dialog"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        template_text = self.text_entry.get("1.0", "end-1c").strip()
        
        # Validate
        if not name:
            messagebox.showerror("Hata", "Şablon adı boş olamaz.")
            return
        
        if not template_text:
            messagebox.showerror("Hata", "Şablon metni boş olamaz.")
            return
        
        # Set result and close
        self.result = (name, description, template_text)
        self.destroy()