# 📚 Multilingual NCERT Doubt-Solver

Production-ready RAG pipeline for NCERT textbook doubt solving with multilingual support.

## ✨ Features
- ✅ Upload & index NCERT PDFs automatically
- 🌐 Supports English, Hindi & 8+ Indian languages
- 🔍 Semantic search with FAISS vector database
- 🤖 Grounded answers (no hallucinations)
- 📱 Clean Streamlit interface
- 📖 Source citation with page numbers

## 🚀 Quick Start

```bash
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env
streamlit run ui/app.py
