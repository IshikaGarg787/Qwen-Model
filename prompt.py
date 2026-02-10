# prompt.py

def build_prompt(context: str, questions: list) -> str:
    """
    Build a strict, clean prompt that returns one plain-text answer per question.
    """

    questions_block = "\n".join(
        f"Q{i+1}: {q}" for i, q in enumerate(questions)
    )

    return f"""
You are a precise assistant.

Rules:
- Answer strictly using the context below
- Do NOT add numbering, bullets, or explanations
- Each answer must be ONE short sentence
- One answer per question, in the SAME order
- If an answer is not present, say exactly:
  No answer found in the document.

Context:
{context}

Questions:
{questions_block}

Answers:
""".strip()
