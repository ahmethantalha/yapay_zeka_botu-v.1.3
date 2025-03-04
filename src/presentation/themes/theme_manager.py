import customtkinter as ctk
import json
import os
from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        self.themes = {
            "light": {
                "bg_color": ["#ffffff", "#ffffff"],
                "fg_color": ["#f2f2f2", "#f2f2f2"],
                "button_color": ["#2986cc", "#2986cc"],
                "button_hover_color": ["#1c578f", "#1c578f"],
                "text_color": ["#000000", "#000000"]
            },
            "dark": {
                "bg_color": ["#2b2b2b", "#2b2b2b"],
                "fg_color": ["#3b3b3b", "#3b3b3b"],
                "button_color": ["#3a7ebf", "#1f538d"],
                "button_hover_color": ["#325882", "#14375e"],
                "text_color": ["#DCE4EE", "#DCE4EE"]
            }
        }
        
        self.current_theme = "dark"
        self._load_theme_settings()
    
    def apply_theme(self, theme_name: str):
        """Apply selected theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            
            # Set customtkinter appearance mode
            ctk.set_appearance_mode("light" if theme_name == "light" else "dark")
            
            # Save theme preference
            self._save_theme_settings()
    
    def get_color(self, color_name: str) -> str:
        """Get color value for current theme"""
        return self.themes[self.current_theme].get(color_name, ["#000000", "#000000"])[0]
    
    def _load_theme_settings(self):
        """Load theme settings from file"""
        try:
            settings_path = os.path.join("data", "theme_settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get("theme", "dark")
        except Exception as e:
            print(f"Tema ayarları yüklenirken hata: {str(e)}")
    
    def _save_theme_settings(self):
        """Save theme settings to file"""
        try:
            os.makedirs("data", exist_ok=True)
            settings_path = os.path.join("data", "theme_settings.json")
            with open(settings_path, 'w') as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception as e:
            print(f"Tema ayarları kaydedilirken hata: {str(e)}")