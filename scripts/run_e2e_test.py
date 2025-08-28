import sys
from src.extractor import extract_text_from_pdf
from src.chunker import chunk_text
from src.embedder import Embedder
from src.indexer import build_faiss_index
from src.retriever import retrieve
from src.llm_agent import answer
import numpy as np
import os

PDF = "data/sample.pdf"

def main():
    if not os.path.exists(PDF):
        print("Please add data/sample.pdf to run e2e test.")
        sys.exit(2)
    pages = extract_text_from_pdf(PDF)
    chunks = []
    for i, p in enumerate(pages):
        for c in chunk_text(p):
            chunks.append({"text": c, "page": i})
    e = Embedder()
    vecs = e.embed([c['text'] for c in chunks]).astype('float32')
    build_faiss_index(vecs, chunks, index_path="data/faiss.index", meta_path="data/meta.pkl")
    res = retrieve("What is the capital of India?")
    if not res:
        print("RETRIEVAL_FAILED")
        sys.exit(1)
    ans = answer("What is the capital of India?", res)
    print("Answer:", ans)
    if "New Delhi" in ans or "new delhi" in ans.lower():
        print("E2E OK")
        sys.exit(0)
    else:
        print("LLM_INCORRECT", ans)
        sys.exit(2)

if __name__ == "__main__":
    main()
