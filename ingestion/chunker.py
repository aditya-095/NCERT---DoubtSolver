from typing import List, Dict, Any
import re

class NCERTTextChunker:
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        for doc_idx, doc in enumerate(documents):
            words = doc['content'].split()
            for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
                chunk_words = words[i:i + self.chunk_size]
                chunk_text = ' '.join(chunk_words)
                
                chunks.append({
                    'content': chunk_text.strip(),
                    'page': doc['page'],
                    'chapter': str(doc.get('chapter', 'Unknown')),
                    'source': doc['source'],
                    'chunk_id': f"doc_{doc_idx}_chunk_{i//self.chunk_size}"
                })
        return chunks
