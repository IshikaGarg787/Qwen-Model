# prompt.py

def build_prompt(pdf_text: str, question: str, max_context_chars: int = 3000) -> str:
    """
    Build a strict, PDF-only prompt for Qwen.
    """
    context = pdf_text[:max_context_chars].strip()

    prompt = f"""
You are a precise assistant. Answer the question strictly using the context below.
Do NOT add any information that is NOT in the context.
If the answer is not in the context, respond with "No answer found in the document."

Context:
{context}

Question:
{question}

Answer concisely in one sentence or phrase.
"""
    return prompt.strip()
