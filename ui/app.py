import streamlit as st
import sys
import os
from datetime import datetime

st.set_page_config(page_title="NCERT GPT", page_icon="🤖", layout="wide")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.pipeline import NCERTRAGPipeline

# FIXED CSS - Text VISIBLE
st.markdown("""
<style>
.chat-bubble { 
    padding: 1.2rem 1.5rem; 
    margin: 1rem 0; 
    border-radius: 18px; 
    max-width: 80%; 
    word-wrap: break-word;
    color: #333 !important;
    line-height: 1.6;
    font-size: 15px;
}
.user-bubble { 
    background: linear-gradient(135deg, #10a37f, #0e8a6a) !important; 
    color: white !important;
    margin-left: auto;
    text-align: left;
}
.bot-bubble { 
    background: white !important; 
    color: #333 !important;
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
h1, h2, h3, p, div {
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.markdown("# 🤖 NCERT GPT")
st.markdown("**Perfect NCERT answers • Any language**")

# Sidebar
with st.sidebar:
    st.header("📚 PDF Upload")
    uploaded_file = st.file_uploader("Choose NCERT PDF", type="pdf")
    
    if uploaded_file is not None:
        if st.button("🚀 Start Chat", type="primary"):
            with st.spinner("Loading PDF..."):
                os.makedirs("data/ncert_pdfs", exist_ok=True)
                path = f"data/ncert_pdfs/{uploaded_file.name}"
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                pipeline = NCERTRAGPipeline()
                pipeline.ingest_pdfs([path])
                st.session_state.pipeline = pipeline
                st.session_state.messages = []
                st.rerun()
                st.success("✅ Ready to chat!")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# MAIN CHAT - PERFECTLY VISIBLE
if st.session_state.pipeline:
    st.markdown("---")  # Chat separator
    
    # Show messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-bubble user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask your question (English/తెలుగు/हिंदी)..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)
        
        # Bot response
        with st.spinner("Searching NCERT..."):
            result = st.session_state.pipeline.query(prompt)
            answer = result['answer']
            
            # Store and display
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.markdown(f'<div class="chat-bubble bot-bubble">{answer}</div>', unsafe_allow_html=True)
        
        st.rerun()

else:
    col1, col2 = st.columns(2)
    with col1:
        st.info("👈 **Upload NCERT PDF first**")
    with col2:
        st.markdown("""
        **Test questions:**
        • Newton's first law  
        • న్యూటన్ మొదటి నియమం
        • Photosynthesis in Telugu
        """)
