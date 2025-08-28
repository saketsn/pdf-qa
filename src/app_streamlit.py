import streamlit as st
from src.extractor import extract_text_from_pdf
from src.chunker import chunk_text
from src.embedder import Embedder
from src.indexer import build_faiss_index
from src.retriever import retrieve
from src.llm_agent import answer

import numpy as np
import os

st.set_page_config(page_title="PDF QA", layout="centered")
st.title("PDF Question Answering (Open Source LLMs)")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded:
    tmp_path = "data/tmp.pdf"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.read())
    pages = extract_text_from_pdf(tmp_path)
    st.info(f"Extracted {len(pages)} pages.")
    if st.button("Build index"):
        chunks = []
        for i, p in enumerate(pages):
            for c in chunk_text(p):
                chunks.append({"text": c, "page": i})
        embedder = Embedder()
        vecs = embedder.embed([c['text'] for c in chunks])
        vecs = np.array(vecs).astype('float32')
        os.makedirs("data", exist_ok=True)
        build_faiss_index(vecs, chunks, index_path="data/faiss.index", meta_path="data/meta.pkl")
        st.success("Index built and saved.")
    q = st.text_input("Ask a question about the uploaded PDF")
    if st.button("Ask") and q:
        res = retrieve(q)
        if not res:
            st.warning("The information is not in the document.")
        else:
            ans = answer(q, res)
            st.write("**Answer**")
            st.write(ans)
            st.write("---")
            st.write("**Top Source**")
            st.write(res[0]['metadata'])
