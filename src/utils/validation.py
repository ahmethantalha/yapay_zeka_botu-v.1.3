import re
from typing import List, Tuple, Optional

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    # Check if API key is not empty and has minimum length
    return bool(api_key) and len(api_key) >= 20

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate file size"""
    return file_size <= max_size

def validate_text_length(text: str, min_length: int = 10, max_length: int = 100000) -> bool:
    """Validate text length"""
    text_length = len(text)
    return min_length <= text_length <= max_length

def validate_form(data: dict, required_fields: List[str]) -> Tuple[bool, Optional[str]]:
    """Validate form data"""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Field '{field}' is required"
    
    return True, None