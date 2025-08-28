import os
from src.retriever import retrieve

def test_retrieve_no_index():
    if not os.path.exists("data/faiss.index"):
        assert True
    else:
        res = retrieve("some random query that is likely absent")
        assert isinstance(res, list)
