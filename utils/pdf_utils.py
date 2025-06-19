import fitz  # PyMuPDF

def get_page_count(file):
    """Get the page count of a PDF file-like object or bytes."""
    if isinstance(file, bytes):
        pdf_doc = fitz.open(stream=file, filetype="pdf")
    else:
        pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    count = pdf_doc.page_count
    pdf_doc.close()
    return count