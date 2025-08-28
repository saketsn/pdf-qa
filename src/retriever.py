import faiss
from .embedder import Embedder
from .indexer import load_faiss_index

embedder = Embedder()

def retrieve(query: str, k: int = 3, threshold: float = 0.55, index_path: str = "data/faiss.index", meta_path: str = "data/meta.pkl"):
    qvec = embedder.embed([query])
    faiss.normalize_L2(qvec)
    index, meta = load_faiss_index(index_path=index_path, meta_path=meta_path)
    D, I = index.search(qvec, k)
    scores = D[0].tolist()
    ids = I[0].tolist()
    results = []
    for score, idx in zip(scores, ids):
        if idx == -1:
            continue
        results.append({"score": float(score), "metadata": meta[idx]})
    if not results or results[0]['score'] < threshold:
        return []
    return results
