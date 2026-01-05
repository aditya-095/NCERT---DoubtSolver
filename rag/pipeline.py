from ingestion.pdf_loader import NCERTPDFLoader
from ingestion.chunker import NCERTTextChunker
from ingestion.embedder import NCERTEmbedder
from rag.retriever import NCERTRetriever
from rag.generator import NCERTGenerator
from typing import List, Dict, Any

class NCERTRAGPipeline:
    def __init__(self, index_path: str = "data/vector_index.faiss"):
        self.retriever = NCERTRetriever(index_path)
        self.generator = NCERTGenerator()
    
    def ingest_pdfs(self, pdf_paths: List[str]):
        loader = NCERTPDFLoader()
        chunker = NCERTTextChunker()
        embedder = NCERTEmbedder()
        
        all_docs = []
        for pdf_path in pdf_paths:
            docs = loader.load_pdf(pdf_path)
            all_docs.extend(docs)
        
        chunks = chunker.chunk_documents(all_docs)
        embedded = embedder.embed_documents(chunks)
        embedder.build_vector_store(embedded)
        self.retriever.load_index()
    
    def query(self, question: str) -> Dict[str, Any]:
        contexts = self.retriever.retrieve(question)
        return self.generator.generate_answer(question, contexts)
