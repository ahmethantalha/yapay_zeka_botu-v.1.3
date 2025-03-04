import re
import json

def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at a sentence boundary
    truncated = text[:max_length]
    last_period = truncated.rfind(".")
    
    if last_period > max_length * 0.7:  # If period is reasonably close to desired length
        return truncated[:last_period+1] + "..."
    return truncated + "..."

def extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text"""
    # Try to find JSON within text
    json_match = re.search(r'({[\s\S]*?})', text)
    
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # If no valid JSON found, try to create a simple structure
    return {"text": text}

def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def count_sentences(text: str) -> int:
    """Count sentences in text"""
    return len(re.split(r'[.!?]+', text)) - 1

def calculate_reading_time(text: str, wpm: int = 200) -> int:
    """Calculate reading time in minutes"""
    word_count = count_words(text)
    minutes = word_count / wpm
    return max(1, round(minutes))