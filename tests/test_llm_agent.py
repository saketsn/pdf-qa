from src.llm_agent import answer_with_local_model

def test_llm_refusal_when_no_context():
    out = answer_with_local_model("Who is the president of Mars?", contexts=[])
    assert "not available" in out.lower() or "not in the document" in out.lower()
