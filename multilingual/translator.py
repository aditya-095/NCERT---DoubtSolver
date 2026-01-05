from googletrans import Translator
from langdetect import detect
from typing import Optional
import re

class MultilingualTranslator:
    def __init__(self):
        try:
            self.translator = Translator()
            self.has_translator = True
        except:
            self.has_translator = False
    
    def detect_language(self, text: str) -> str:
        try:
            if not text.strip():
                return 'en'
            lang = detect(text.strip())
            return lang if lang in ['en', 'te', 'hi', 'ta'] else 'en'
        except:
            return 'en'
    
    def detect_target_language(self, query: str) -> str:
        query_lower = query.lower()
        
        telugu_keywords = ['telugu', 'తెలుగు', 'తెలుగులో', 'telegu']
        hindi_keywords = ['hindi', 'हिंदी', 'हिन्दी']
        
        if any(keyword in query_lower for keyword in telugu_keywords):
            return 'te'
        elif any(keyword in query_lower for keyword in hindi_keywords):
            return 'hi'
        return self.detect_language(query)
    
    def translate_to_telugu(self, text: str) -> str:
        if not self.has_translator:
            return self.telugu_fallback(text)
        try:
            result = self.translator.translate(text, dest='te')
            return result.text
        except:
            return self.telugu_fallback(text)
    
    def telugu_fallback(self, text: str) -> str:
        return text.replace("Answer", "సమాధానం").replace("Explanation", "వివరణ")
    
    def translate(self, text: str, target_lang: str) -> str:
        if target_lang == 'te':
            return self.translate_to_telugu(text)
        return text
