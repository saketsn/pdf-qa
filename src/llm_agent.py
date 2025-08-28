import os
from typing import List
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_API_TOKEN", None)
USE_HF_API = bool(HF_TOKEN)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

LOCAL_MODEL = os.getenv("LOCAL_LLM_MODEL", "google/flan-t5-small")
_local_tokenizer = None
_local_model = None

PROMPT_TEMPLATE = """
You are an assistant that answers only using the provided context. 
If the answer is not contained in the context, respond exactly with:
"The information is not available in the document."
Context:
{context}

Question: {question}
Answer:
"""

def _load_local_model():
    global _local_tokenizer, _local_model
    if _local_model is None:
        _local_tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
        _local_model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_MODEL)
    return _local_tokenizer, _local_model


def answer_with_local_model(question: str, contexts: List[dict], max_len: int = 128) -> str:
    tokenizer, model = _load_local_model()
    context_text = "\n\n".join([c['metadata']['text'] for c in contexts])
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(**inputs, max_new_tokens=max_len)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def answer_with_hf_api(question: str, contexts: List[dict], model: str = "google/flan-t5-base", max_len: int = 128) -> str:
    client = InferenceClient(api_key=HF_TOKEN)
    context_text = "\n\n".join([c['metadata']['text'] for c in contexts])
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)
    resp = client.text_generation(model=model, inputs=prompt, max_new_tokens=max_len)
    if isinstance(resp, list) and resp:
        return resp[0].get('generated_text', str(resp))
    if isinstance(resp, dict):
        return resp.get('generated_text', str(resp))
    return str(resp)

def answer(question: str, contexts: List[dict]):
    if USE_HF_API:
        try:
            return answer_with_hf_api(question, contexts)
        except Exception:
            return answer_with_local_model(question, contexts)
    else:
        return answer_with_local_model(question, contexts)
