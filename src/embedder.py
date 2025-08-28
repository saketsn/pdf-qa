from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # 384-d

class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
    def embed(self, texts):
        vecs = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return vecs.astype('float32')
