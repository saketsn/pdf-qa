import faiss
import numpy as np
import pickle
from typing import List, Dict

def build_faiss_index(vectors: np.ndarray, metadata: List[Dict], index_path: str = "data/faiss.index", meta_path: str = "data/meta.pkl"):
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)    # inner product on normalized vectors => cosine
    faiss.normalize_L2(vectors)
    index.add(vectors)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)
    return index

def load_faiss_index(index_path: str = "data/faiss.index", meta_path: str = "data/meta.pkl"):
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    return index, meta
