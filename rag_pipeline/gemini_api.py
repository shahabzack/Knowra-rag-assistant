import google.generativeai as genai
from dotenv import load_dotenv
import os

class GeminiClient:
    def __init__(self):
        """Initialize Gemini API client."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate a response using Gemini API with query and context."""
        prompt = f"Answer the following question based on the provided context. If the context doesn't fully address the question, use your knowledge to provide a concise and accurate answer.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        response = self.model.generate_content(prompt)
        return response.text