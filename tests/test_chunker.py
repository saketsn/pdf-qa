from src.chunker import chunk_text

def test_chunk_overlap():
    text = "a"*2000
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    assert chunks[0][-100:] == chunks[1][:100]
