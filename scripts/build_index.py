import argparse
from src.extractor import extract_text_from_pdf
from src.chunker import chunk_text
from src.embedder import Embedder
from src.indexer import build_faiss_index
import numpy as np
import os

def main(pdf_path: str, out_index: str = "data/faiss.index", out_meta: str = "data/meta.pkl"):
    pages = extract_text_from_pdf(pdf_path)
    chunks = []
    for i, p in enumerate(pages):
        for c in chunk_text(p):
            chunks.append({"text": c, "page": i})
    if not chunks:
        print("No chunks extracted. Exiting.")
        return
    e = Embedder()
    texts = [c['text'] for c in chunks]
    vecs = e.embed(texts).astype('float32')
    os.makedirs(os.path.dirname(out_index) or ".", exist_ok=True)
    build_faiss_index(vecs, chunks, index_path=out_index, meta_path=out_meta)
    print(f"Index built: {out_index}. Meta: {out_meta}. Chunks: {len(chunks)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, help="path to input pdf")
    parser.add_argument("--index", default="data/faiss.index")
    parser.add_argument("--meta", default="data/meta.pkl")
    args = parser.parse_args()
    main(args.pdf, args.index, args.meta)
