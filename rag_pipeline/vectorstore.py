from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

def create_vector_store(documents: List) -> FAISS:
    """Create FAISS vector store from documents using locally stored embeddings."""
    
    # Use locally downloaded model path
    embeddings = HuggingFaceEmbeddings(model_name="models/all-MiniLM-L6-v2")
    
    # Create FAISS vector store
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store
