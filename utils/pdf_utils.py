import fitz  # PyMuPDF
from PIL import Image
import io

def convert_page_to_image(pdf_bytes, page_number, dpi=150):
    """Convert a specific PDF page to a PIL Image."""
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if page_number < 0 or page_number >= pdf_doc.page_count:
        pdf_doc.close()
        return None
    page = pdf_doc[page_number]
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    pdf_doc.close()
    return img

def get_page_count(file):
    """Get the page count of a PDF file-like object or bytes."""
    if isinstance(file, bytes):
        pdf_doc = fitz.open(stream=file, filetype="pdf")
    else:
        pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    count = pdf_doc.page_count
    pdf_doc.close()
    return count