from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def create_rag_chain():
    """
    Creates the core part of the RAG chain (prompt + LLM)
    that generates an answer based on context.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file. Please check your .env file.")
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.2)
    
    
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Answer the user's question based ONLY on the following context.
If the context does not contain the answer, state clearly that the answer is not found in the provided pages.
Do not use any external knowledge. Be concise.

Context:
{context}

Question: {input}

Answer:"""
    )
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    return document_chain