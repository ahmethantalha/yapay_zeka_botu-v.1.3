import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional, Callable
from src.repositories.custom_analysis_repository import CustomAnalysisRepository
from src.models.custom_analysis_type import CustomAnalysisType

class CustomAnalysisWindow(ctk.CTkToplevel):
    """Window for managing custom analysis types"""
    def __init__(self, parent, analysis_repo: CustomAnalysisRepository, on_types_changed: Optional[Callable] = None):
        super().__init__(parent)
        
        self.analysis_repo = analysis_repo
        self.on_types_changed = on_types_changed
        
        # Configure window
        self.title("Özel Analiz Türleri")
        self.geometry("700x600")
        
        # Create layout
        self._create_layout()
        
        # Load analysis types
        self._load_analysis_types()
    
    def _create_layout(self):
        """Create window layout"""
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Özel Analiz Türleri",
            font=("Arial", 18, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Add button
        add_button = ctk.CTkButton(
            header_frame,
            text="Yeni Analiz Türü Ekle",
            command=self._add_analysis_type
        )
        add_button.pack(side="right", padx=10)
        
        # Analysis types list
        self.types_frame = ctk.CTkScrollableFrame(self)
        self.types_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    
    def _load_analysis_types(self):
        """Load custom analysis types"""
        try:
            # Clear current items
            for widget in self.types_frame.winfo_children():
                widget.destroy()
            
            # Get all custom analysis types
            custom_types = self.analysis_repo.get_all()
            
            if not custom_types:
                no_types_label = ctk.CTkLabel(
                    self.types_frame,
                    text="Henüz özel analiz türü bulunmuyor. Yeni bir tür ekleyin.",
                    font=("Arial", 14)
                )
                no_types_label.pack(pady=20)
                return
            
            # Add items
            for i, custom_type in enumerate(custom_types):
                type_item = AnalysisTypeItem(
                    self.types_frame,
                    custom_type=custom_type,
                    on_edit=self._edit_analysis_type,
                    on_delete=self._delete_analysis_type,
                    fg_color="#2f2f2f" if i % 2 == 0 else "#3f3f3f"
                )
                type_item.pack(fill="x", pady=5)
        
        except Exception as e:
            messagebox.showerror("Hata", f"Analiz türleri yüklenirken hata oluştu: {str(e)}")
    
    def _add_analysis_type(self):
        """Add new custom analysis type"""
        dialog = AnalysisTypeDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            name, description, prompt_template = dialog.result
            
            try:
                self.analysis_repo.create_custom_type(name, description, prompt_template)
                self._load_analysis_types()
                
                # Notify parent
                if self.on_types_changed:
                    self.on_types_changed()
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Analiz türü eklenirken hata oluştu: {str(e)}")
    
    def _edit_analysis_type(self, custom_type: CustomAnalysisType):
        """Edit custom analysis type"""
        dialog = AnalysisTypeDialog(
            self, 
            name=custom_type.name,
            description=custom_type.description,
            prompt_template=custom_type.prompt_template
        )
        self.wait_window(dialog)
        
        if dialog.result:
            name, description, prompt_template = dialog.result
            
            try:
                self.analysis_repo.update_custom_type(custom_type.name, description, prompt_template)
                self._load_analysis_types()
                
                # Notify parent
                if self.on_types_changed:
                    self.on_types_changed()
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Analiz türü güncellenirken hata oluştu: {str(e)}")
    
    def _delete_analysis_type(self, name: str):
        """Delete custom analysis type"""
        confirm = messagebox.askyesno(
            "Onay", 
            f"'{name}' analiz türünü silmek istediğinizden emin misiniz?"
        )
        
        if confirm:
            try:
                self.analysis_repo.delete_by_name(name)
                self._load_analysis_types()
                
                # Notify parent
                if self.on_types_changed:
                    self.on_types_changed()
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Analiz türü silinirken hata oluştu: {str(e)}")

class AnalysisTypeItem(ctk.CTkFrame):
    """Single analysis type item widget"""
    def __init__(self, parent, custom_type: CustomAnalysisType, 
                 on_edit: Callable[[CustomAnalysisType], None], 
                 on_delete: Callable[[str], None], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.custom_type = custom_type
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._create_layout()
    
    def _create_layout(self):
        """Create item layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Name and description
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.custom_type.name,
            font=("Arial", 14, "bold")
        )
        name_label.pack(anchor="w")
        
        if self.custom_type.description:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=self.custom_type.description,
                font=("Arial", 10),
                wraplength=600
            )
            desc_label.pack(anchor="w", pady=(0, 5))
        
        # Prompt preview
        preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        prompt_preview = self.custom_type.prompt_template
        if len(prompt_preview) > 100:
            prompt_preview = prompt_preview[:100] + "..."
        
        preview_label = ctk.CTkLabel(
            preview_frame,
            text=f"Şablon: {prompt_preview}",
            font=("Arial", 10),
            wraplength=600
        )
        preview_label.pack(anchor="w")
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="Düzenle",
            width=80,
            command=self._on_edit
        )
        edit_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Sil",
            width=80,
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self._on_delete
        )
        delete_button.pack(side="left", padx=5)
    
    def _on_edit(self):
        """Handle edit button click"""
        if self.on_edit:
            self.on_edit(self.custom_type)
    
    def _on_delete(self):
        """Handle delete button click"""
        if self.on_delete:
            self.on_delete(self.custom_type.name)

class AnalysisTypeDialog(ctk.CTkToplevel):
    """Dialog for adding/editing custom analysis types"""
    def __init__(self, parent, name: str = "", description: str = "", prompt_template: str = ""):
        super().__init__(parent)
        
        # Configure dialog
        self.title("Analiz Türü " + ("Düzenle" if name else "Ekle"))
        self.geometry("600x500")
        self.resizable(True, True)
        
        # Initial values
        self.name = name
        self.description = description
        self.prompt_template = prompt_template
        
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
            text="Analiz Türü Adı:",
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
            # Editing existing analysis type, disable name field
            self.name_entry.configure(state="disabled")
        
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
            text="Prompt Şablonu:",
            font=("Arial", 12, "bold")
        )
        self.text_label.pack(anchor="w", pady=(0, 5))
        
        # Template help button
        self.help_button = ctk.CTkButton(
            self.main_frame,
            text="Prompt Yazma Rehberi",
            command=self._show_prompt_help
        )
        self.help_button.pack(anchor="w", pady=(0, 5))
        
        self.text_entry = ctk.CTkTextbox(
            self.main_frame,
            width=560,
            height=250
        )
        self.text_entry.pack(fill="both", expand=True, pady=(0, 10))
        if self.prompt_template:
            self.text_entry.insert("1.0", self.prompt_template)
        
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
        """Save analysis type and close dialog"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        prompt_template = self.text_entry.get("1.0", "end-1c").strip()
        
        # Validate
        if not name:
            messagebox.showerror("Hata", "Analiz türü adı boş olamaz.")
            return
        
        if not prompt_template:
            messagebox.showerror("Hata", "Prompt şablonu boş olamaz.")
            return
        
        # Set result and close
        self.result = (name, description, prompt_template)
        self.destroy()
    
    def _show_prompt_help(self):
        """Show prompt writing guide"""
        help_text = """Etkili Prompt Yazma Rehberi:

1. Açık ve net olun:
   - Ne istediğinizi kesin bir dille belirtin
   - Adım adım talimatlar verin

2. Bağlam ekleyin:
   - Amacınızı belirtin
   - Arka plan bilgisi verin

3. Format belirtin:
   - İstediğiniz çıktı formatını tanımlayın
   - Örnekler verin

4. Özel talimatlar ekleyin:
   - Odaklanılması gereken noktaları belirtin
   - Kaçınılması gereken şeyleri belirtin

5. Prompt şablonunda "{text}" ifadesini kullanın:
   - Bu, analiz edilecek metin ile değiştirilecektir

Örnek:
\"\"\"
Aşağıdaki metni bilimsel bir bakış açısıyla analiz edin:
{text}

Lütfen şu yapıda bir analiz sağlayın:
1. Temel bilimsel kavramlar
2. Metodoloji değerlendirmesi
3. Sonuçların geçerliliği
4. Önerilen iyileştirmeler
\"\"\"
"""
        
        help_dialog = ctk.CTkToplevel(self)
        help_dialog.title("Prompt Yazma Rehberi")
        help_dialog.geometry("600x500")
        help_dialog.transient(self)
        help_dialog.grab_set()
        
        help_text_box = ctk.CTkTextbox(help_dialog)
        help_text_box.pack(fill="both", expand=True, padx=20, pady=20)
        help_text_box.insert("1.0", help_text)
        help_text_box.configure(state="disabled")