from langdetect import detect
from typing import Optional

class LanguageDetector:
    SUPPORTED_LANGUAGES = ['en', 'te', 'hi', 'ta', 'kn']
    
    @staticmethod
    def detect_language(text: str) -> str:
        try:
            if not text.strip():
                return 'en'
            lang = detect(text.strip())
            return lang if lang in LanguageDetector.SUPPORTED_LANGUAGES else 'en'
        except:
            return 'en'
