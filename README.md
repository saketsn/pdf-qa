#  PDF Question Answering System using Open-Source LLMs

This project allows you to **upload a PDF document** and then **ask questions in natural English** about its content.
The system extracts the text from the PDF, indexes it, and uses a **Hugging Face LLM** to generate meaningful answers.

---
##  Features
- Extracts text from PDFs using **pdfplumber**
- Splits content into **chunks** for better retrieval
- Uses **FAISS** for fast similarity search
- Leverages **Hugging Face Transformers API** to answer questions
- CLI-based interaction: ask questions and get AI-generated answers
- Modular, extensible, and easy to use

---
##  Project Structure

![alt text](image.png)
![alt text](image-1.png)