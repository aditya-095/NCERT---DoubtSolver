from typing import List, Dict, Any
from multilingual.translator import MultilingualTranslator
import re

class NCERTGenerator:
    def __init__(self):
        self.translator = MultilingualTranslator()
    
    def clean_explanation(self, content: str) -> str:
        # Remove headers, equations, extra symbols
        content = re.sub(r'^\d+\.\d+\s+', '', content)
        content = re.sub(r'\([^)]*\)', '', content)
        content = re.sub(r'\[.*?\]', '', content)
        content = re.sub(r'CHAPTER\s+\w+', '', content)
        
        # Get first 3 meaningful sentences
        sentences = re.split(r'[.!?]+', content)
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                clean_sentences.append(sentence)
                if len(clean_sentences) >= 3:
                    break
        
        return ' '.join(clean_sentences)[:500].strip()
    
    def generate_answer(self, query: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        target_lang = self.translator.detect_target_language(query)
        
        if not contexts:
            no_answer = {
                'en': "**No relevant NCERT content found.**",
                'te': "**NCERT పాఠ్యపుస్తకంలో సంబంధిత కంటెంట్ దొరకలేదు.**"
            }
            return {'answer': no_answer.get(target_lang, no_answer['en'])}
        
        # Clean best explanation
        best_content = self.clean_explanation(contexts[0]['content'])
        
        # Headers by language
        headers = {
            'en': "**📚 NCERT Explanation**",
            'te': "**📚 NCERT తెలుగు వివరణ**",
            'hi': "**📚 NCERT हिंदी व्याख्या**"
        }
        
        final_explanation = self.translator.translate(best_content, target_lang)
        answer = f"{headers.get(target_lang, headers['en'])}\n\n{final_explanation}"
        
        return {'answer': answer}
