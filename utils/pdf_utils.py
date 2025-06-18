import fitz  # PyMuPDF
from PIL import Image
import io

def convert_pdf_to_images(file, dpi=150):
    """Converts a PDF file-like object to a list of PIL Images."""
    images = []
    # The file object from streamlit is already in bytes, no need to read it again if passed correctly
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf_doc:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    return images

def get_page_count(file):
    """Gets the page count of a PDF file-like object."""
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    return pdf_doc.page_count