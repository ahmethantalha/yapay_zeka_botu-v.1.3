from typing import Optional, Dict, Any, List
import json
from src.repositories.ai_config_repository import AIConfigRepository
from src.repositories.prompt_repository import PromptRepository
from src.core.security import Security
import customtkinter as ctk
import os

class SettingsViewModel:
    def __init__(self, 
                ai_config_repo: AIConfigRepository,
                prompt_repo: PromptRepository,
                security: Security):
        self.ai_config_repo = ai_config_repo
        self.prompt_repo = prompt_repo
        self.security = security
        
        # State
        self.current_theme = "dark"
        self.font_size = 12
        
        # Dosya işleme ayarları
        self.file_processing_settings = {
            'auto_split': False,
            'chunk_size': 3,
            'min_split_size': 1,
            'combine_method': 'sequential',
            'parallel_processing': False,
            'enable_cache': True
        }
        
        # Callbacks
        self._on_settings_saved = None
        self._on_error = None
        
        # Settings dosyasından ayarları yükle
        self._load_settings()
    
    def set_callbacks(self, on_settings_saved, on_error):
        self._on_settings_saved = on_settings_saved
        self._on_error = on_error
    
    def get_ai_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all AI configurations"""
        configs = {}
        for config in self.ai_config_repo.get_all():
            settings = json.loads(config.settings) if config.settings else {}
            if 'api_key' in settings:
                settings['api_key'] = self.security.decrypt(settings['api_key'])
            
            configs[config.provider] = {
                'is_active': config.is_active,
                'model_name': config.model_name,
                'max_tokens': config.max_tokens,
                'temperature': config.temperature,
                **settings
            }
        
        return configs
    
    def save_ai_config(self, provider: str, config: Dict[str, Any]):
        """Save AI configuration"""
        try:
            if 'api_key' in config:
                config['api_key'] = self.security.encrypt(config['api_key'])
            
            self.ai_config_repo.update_config(provider, config)
            
            if self._on_settings_saved:
                self._on_settings_saved()
                
        except Exception as e:
            if self._on_error:
                self._on_error(str(e))
    
    def get_prompt_templates(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all prompt templates for user"""
        templates = []
        for template in self.prompt_repo.get_by_user(user_id):
            templates.append({
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'template_text': template.template_text
            })
        
        return templates
    
    def save_prompt_template(self, user_id: int, name: str, 
                           description: str, template_text: str):
        """Save prompt template"""
        try:
            template = self.prompt_repo.get_by_name(user_id, name)
            
            if template:
                template.description = description
                template.template_text = template_text
                self.prompt_repo.update(template)
            else:
                from src.models.prompt_template import PromptTemplate
                template = PromptTemplate(
                    user_id=user_id,
                    name=name,
                    description=description,
                    template_text=template_text
                )
                self.prompt_repo.create(template)
            
            if self._on_settings_saved:
                self._on_settings_saved()
                
        except Exception as e:
            if self._on_error:
                self._on_error(str(e))

    def get_current_theme(self) -> str:
        """Get current theme"""
        return self.current_theme
    
    def set_theme(self, theme: str):
        """Set theme and apply"""
        self.current_theme = theme
        ctk.set_appearance_mode(theme)
        self._save_settings()

    def get_setting(self, key: str, default=None):
        """Get file processing setting"""
        return self.file_processing_settings.get(key, default)

    def save_file_processing_settings(self, settings: dict):
        """Save file processing settings"""
        try:
            self.file_processing_settings.update(settings)
            self._save_settings()
            
            if self._on_settings_saved:
                self._on_settings_saved()
                
        except Exception as e:
            if self._on_error:
                self._on_error(str(e))

    def _load_settings(self):
        """Load settings from file"""
        try:
            with open('data/settings.json', 'r') as f:
                settings = json.load(f)
                self.current_theme = settings.get('theme', 'dark')
                self.file_processing_settings.update(
                    settings.get('file_processing', {})
                )
        except:
            # Dosya yoksa veya okuma hatası olursa varsayılan ayarları kullan
            pass

    def _save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'theme': self.current_theme,
                'file_processing': self.file_processing_settings
            }
            
            os.makedirs('data', exist_ok=True)
            with open('data/settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
                
        except Exception as e:
            if self._on_error:
                self._on_error(f"Ayarlar kaydedilirken hata: {str(e)}")