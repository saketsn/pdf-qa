import re
from typing import List, Iterator

def clean_text(text: str) -> str:
    """
    Clean the input text by normalizing whitespace and line breaks.
    """
    text = re.sub(r'\r\n', '\n', text)       # Convert Windows line endings to \n
    text = re.sub(r'\n+', ' ', text)         # Replace multiple newlines with space
    text = re.sub(r'\s{2,}', ' ', text)      # Replace multiple spaces with single space
    return text.strip()

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200) -> List[str]:
    """
    Split text into chunks of size `chunk_size` with `overlap`.
    Returns a list of chunks.
    """
    text = clean_text(text)
    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        chunks.append(chunk)

        if end == n:
            break  # Stop if we reached the end

        start = end - overlap

    return chunks

def chunk_text_generator(text: str, chunk_size: int = 800, overlap: int = 200) -> Iterator[str]:
    """
    Generator version of chunk_text.
    Yields chunks one by one to save memory for large texts.
    """
    text = clean_text(text)
    if not text:
        return

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        yield text[start:end]

        if end == n:
            break

        start = end - overlap

# Example usage
if __name__ == "__main__":
    sample_text = 'a' * 2000
    print("List-based chunks:")
    print(chunk_text(sample_text, chunk_size=500, overlap=100)[:2])

    print("\nGenerator-based chunks:")
    for i, chunk in enumerate(chunk_text_generator(sample_text, chunk_size=500, overlap=100)):
        if i < 2:
            print(chunk)
        else:
            break
