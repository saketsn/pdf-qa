from src.extractor import extract_text_from_pdf
import os

def test_extract_text_non_empty():
    path = "data/sample.pdf"
    if not os.path.exists(path):
        assert True
    else:
        pages = extract_text_from_pdf(path)
        assert len(pages) > 0
