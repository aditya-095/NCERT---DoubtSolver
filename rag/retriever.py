import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import pickle
import os

class NCERTRetriever:
    def __init__(self, index_path: str = "data/vector_index.faiss"):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.index_path = index_path
        self.index = None
        self.docstore = {}
    
    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.index_path.replace('.faiss', '_docstore.pkl')):
            self.index = faiss.read_index(self.index_path)
            with open(self.index_path.replace('.faiss', '_docstore.pkl'), 'rb') as f:
                self.docstore = pickle.load(f)
    
    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        self.load_index()
        if not self.index:
            return []
        
        query_emb = self.model.encode([query]).astype('float32')
        faiss.normalize_L2(query_emb)
        scores, indices = self.index.search(query_emb, k)
        
        results = []
        doc_keys = list(self.docstore.keys())
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(doc_keys):
                chunk = self.docstore[doc_keys[idx]].copy()
                chunk['score'] = float(score)
                results.append(chunk)
        return results
