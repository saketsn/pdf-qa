import pdfplumber
from typing import List

def extract_text_from_pdf(path: str) -> List[str]:
    pages = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or "")
    return pages
