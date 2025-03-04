import os
import shutil
from typing import List, Set

def get_file_extension(file_path: str) -> str:
    """Get file extension with dot"""
    return os.path.splitext(file_path)[1].lower()

def is_valid_file_type(file_path: str, valid_extensions: Set[str]) -> bool:
    """Check if file is a valid type"""
    ext = get_file_extension(file_path)
    return ext in valid_extensions

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)

def create_temp_file(original_file: str, temp_dir: str) -> str:
    """Create a copy of file in temp directory"""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_name = os.path.basename(original_file)
    temp_file = os.path.join(temp_dir, file_name)
    
    shutil.copy2(original_file, temp_file)
    return temp_file

def clean_temp_files(temp_dir: str, file_pattern: str = None):
    """Clean temporary files"""
    if not os.path.exists(temp_dir):
        return
    
    if file_pattern:
        for file in os.listdir(temp_dir):
            if file_pattern in file:
                os.remove(os.path.join(temp_dir, file))
    else:
        # Clean all files in temp dir
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)