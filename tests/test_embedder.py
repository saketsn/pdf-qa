from src.embedder import Embedder

def test_embed_shape():
    e = Embedder()
    v = e.embed(["hello","world"])
    assert v.shape[1] == 384
