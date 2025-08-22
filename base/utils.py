# core/utils.py
import io
from typing import Optional

import easyocr
from PIL import Image
import numpy as np

# PDF libs
import pdfplumber
# import fitz  # PyMuPDF

# ---- EasyOCR reader (singleton) ----
# Matches your notebook: reader = easyocr.Reader(['en'])
# Add more languages if needed, e.g. ['en', 'hi'] for Hindi, etc.
_READER: Optional[easyocr.Reader] = None

def get_reader(lang_list=None) -> easyocr.Reader:
    global _READER
    if _READER is None:
        _READER = easyocr.Reader(lang_list or ['en'])
    return _READER

# ---- Image OCR (from your notebook, cleaned for backend) ----
def extract_text_from_image(file_bytes: bytes, languages=None) -> str:
    """
    OCR an image (PNG/JPG/etc.) using EasyOCR.
    """
    # Ensure image is loadable
    _ = Image.open(io.BytesIO(file_bytes)).convert("RGB")  # validates bytes

    reader = get_reader(languages or ['en'])
    # Your notebook used: reader.readtext(processed_image, detail=0)
    # We can pass raw bytes; EasyOCR accepts numpy arrays as well.
    img = np.array(_)
    results = reader.readtext(img, detail=0)
    return " ".join([r.strip() for r in results if str(r).strip()])

# ---- PDF text extraction with OCR fallback ----
def extract_text_from_pdf(file_bytes: bytes, languages=None) -> str:
    """
    1) Try text extraction via pdfplumber (for digital/text PDFs).
    2) If no text found, render pages to images and OCR each page (image-based PDFs).
    """
    text_chunks = []

    # 1) Try text extraction first
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                if t.strip():
                    text_chunks.append(t)
    except Exception:
        # If pdfplumber fails, we'll rely entirely on OCR below
        pass

    if "".join(text_chunks).strip():
        return "\n\n".join(text_chunks)

    # 2) OCR fallback: render pages as images and OCR
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        ocr_chunks = []
        for page in doc:
            # Render to image (PNG) then OCR
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            page_text = extract_text_from_image(img_bytes, languages=languages)
            if page_text.strip():
                ocr_chunks.append(page_text)
        return "\n\n".join(ocr_chunks)
    except Exception:
        return ""

# ---- Simple LaTeX templating ----
def fill_template(template: str, content: str) -> str:
    """
    Replace {{content}} placeholder in LaTeX template with extracted/provided text.
    (You can expand this into a safer templating layer later.)
    """
    return template.replace("{{content}}", content or "")
