import json
import os
from typing import List, Dict
from datetime import datetime

class RecentFiles:
    def __init__(self, max_files: int = 10):
        self.max_files = max_files
        self.recent_files: List[Dict] = []
        self._load_recent_files()
    
    def add_file(self, file_path: str, analysis_type: str = None):
        """Add file to recent files list"""
        # Remove if already exists
        self.recent_files = [f for f in self.recent_files if f["path"] != file_path]
        
        # Add to beginning of list
        self.recent_files.insert(0, {
            "path": file_path,
            "name": os.path.basename(file_path),
            "date": datetime.now().isoformat(),
            "analysis_type": analysis_type
        })
        
        # Keep only max_files
        self.recent_files = self.recent_files[:self.max_files]
        
        # Save changes
        self._save_recent_files()
    
    def get_recent_files(self) -> List[Dict]:
        """Get list of recent files"""
        # Filter out files that no longer exist
        self.recent_files = [f for f in self.recent_files 
                           if os.path.exists(f["path"])]
        return self.recent_files
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.recent_files = []
        self._save_recent_files()
    
    def _load_recent_files(self):
        """Load recent files from storage"""
        try:
            recent_file_path = os.path.join("data", "recent_files.json")
            if os.path.exists(recent_file_path):
                with open(recent_file_path, 'r', encoding='utf-8') as f:
                    self.recent_files = json.load(f)
        except Exception as e:
            print(f"Son kullanılan dosyalar yüklenirken hata: {str(e)}")
    
    def _save_recent_files(self):
        """Save recent files to storage"""
        try:
            os.makedirs("data", exist_ok=True)
            recent_file_path = os.path.join("data", "recent_files.json")
            with open(recent_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.recent_files, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Son kullanılan dosyalar kaydedilirken hata: {str(e)}")