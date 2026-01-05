from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any
import pickle
import os

class NCERTEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        texts = [doc['content'] for doc in documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        for i, doc in enumerate(documents):
            doc['embedding'] = embeddings[i].tolist()
        return documents
    
    def build_vector_store(self, documents: List[Dict[str, Any]], index_path: str = "data/vector_index.faiss"):
        embeddings = np.array([doc['embedding'] for doc in documents]).astype('float32')
        faiss.normalize_L2(embeddings)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(index, index_path)
        with open(index_path.replace('.faiss', '_docstore.pkl'), 'wb') as f:
            pickle.dump({doc['chunk_id']: doc for doc in documents}, f)
