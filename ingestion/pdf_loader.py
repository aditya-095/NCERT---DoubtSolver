import fitz
import os
from typing import List, Dict, Any
from pathlib import Path

class NCERTPDFLoader:
    def __init__(self, pdf_dir: str = "data/ncert_pdfs"):
        self.pdf_dir = Path(pdf_dir)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
    
    def load_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        doc = fitz.open(file_path)
        documents = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text").strip()
            
            if len(text) > 50:  # Skip empty pages
                documents.append({
                    'content': text,
                    'page': page_num + 1,
                    'chapter': text.split('\n')[:2],
                    'source': os.path.basename(file_path)
                })
        doc.close()
        return documents
