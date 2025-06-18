from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from io import BytesIO
import os

def load_and_split_pdf(file: BytesIO, filename: str) -> List:
    """
    Loads an entire PDF and splits it into chunks.
    PyPDFLoader automatically adds 'page' metadata to each document chunk.
    """
    # Create a temporary directory to store the file for processing
    os.makedirs("temp_data", exist_ok=True)
    temp_path = os.path.join("temp_data", filename)
    
    with open(temp_path, "wb") as f:
        f.write(file.getvalue())

    # Load the PDF. Each page becomes a Document with metadata {'source': ..., 'page': N}
    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    # Split the documents into smaller chunks for the vector store
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    
    # Clean up the temporary file
    try:
        os.remove(temp_path)
    except OSError as e:
        print(f"Error removing temporary file {temp_path}: {e}")
        
    return chunks