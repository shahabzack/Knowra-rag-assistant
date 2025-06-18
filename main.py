from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import io
from utils.document_loader import load_and_split_pdf
from rag_pipeline.vectorstore import create_vector_store
from rag_pipeline.rag_chain import create_rag_chain
from langchain.chains import create_retrieval_chain
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

# --- App Initialization ---
app = FastAPI(title="RAG PDF Chatbot API")

# --- In-Memory Storage ---
vector_stores = {}
document_chain = create_rag_chain()

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    question: str
    filename: str
    start_page: int
    end_page: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[int]

# --- API Endpoints ---
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files allowed"})
    
    content = await file.read()
    documents = load_and_split_pdf(io.BytesIO(content), file.filename)
    if not documents:
        raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")
        
    vector_stores[file.filename] = create_vector_store(documents)
    return {"message": f"PDF '{file.filename}' processed successfully."}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if request.filename not in vector_stores:
        raise HTTPException(status_code=404, detail=f"PDF '{request.filename}' not found. Please upload it first.")

    # Handle greetings
    normalized_question = request.question.lower().strip().rstrip("!?.")
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    if normalized_question in greetings:
        return ChatResponse(
            answer="Hello! I'm ready to answer questions about your document. What would you like to know?",
            sources=[]  # No sources for a greeting
        )

    # Create retriever with page filtering
    vector_store = vector_stores[request.filename]
    retriever = vector_store.as_retriever(search_kwargs={"k": 7})

    class PageFilteredRetriever(BaseRetriever):
        base_retriever: BaseRetriever
        start_page: int
        end_page: int

        async def _aget_relevant_documents(self, query: str) -> List[Document]:
            docs = await self.base_retriever.aget_relevant_documents(query)
            return [
                doc for doc in docs 
                if self.start_page <= doc.metadata.get('page', -1) <= self.end_page
            ]

        def _get_relevant_documents(self, query: str) -> List[Document]:
            docs = self.base_retriever.get_relevant_documents(query)
            return [
                doc for doc in docs 
                if self.start_page <= doc.metadata.get('page', -1) <= self.end_page
            ]

    filtered_retriever = PageFilteredRetriever(
        base_retriever=retriever,
        start_page=request.start_page,
        end_page=request.end_page
    )

    # Create the retrieval chain
    full_chain = create_retrieval_chain(filtered_retriever, document_chain)

    # Run the RAG chain
    response = await full_chain.ainvoke({"input": request.question})
    
    answer = response.get("answer", "An error occurred during processing.")
    context_docs = response.get("context", [])

    # Handle questions not in the PDF
    not_found_phrases = [
        "not found", 
        "cannot answer", 
        "do not contain the answer", 
        "not in the provided context",
        "i cannot answer"
    ]
    if any(phrase in answer.lower() for phrase in not_found_phrases):
        return ChatResponse(
            answer="I can only answer questions based on the content of the document you provided. Please ask something related to the PDF.",
            sources=[]  # No sources if the answer wasn't found
        )
    
    # Extract sources
    sources = sorted(list(set(doc.metadata.get("page", -1) + 1 for doc in context_docs)))
    
    return ChatResponse(answer=answer, sources=sources)