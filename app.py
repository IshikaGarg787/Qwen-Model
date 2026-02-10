from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from mangum import Mangum
import re

from pdf_utils import download_pdf, extract_text_from_pdf
from model_runner import ask_model

# ----------------------------
# App + CORS
# ----------------------------
app = FastAPI(title="AI Battle Arena")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request / Response Models
# ----------------------------
class BattleRequest(BaseModel):
    pdf_url: str
    questions: List[str]

class BattleResponse(BaseModel):
    answers: List[str]

# ----------------------------
# API Endpoint
# ----------------------------
@app.post("/aibattle", response_model=BattleResponse)
def aibattle(req: BattleRequest):

    # 1️⃣ Download + extract PDF
    try:
        pdf_path = download_pdf(req.pdf_url)
        pages = extract_text_from_pdf(pdf_path)
    except Exception as e:
        return BattleResponse(
            answers=[f"Error fetching PDF: {str(e)}"] * len(req.questions)
        )

    # 2️⃣ Combine all PDF text into single string
    all_text = "\n".join([p["text"] for p in pages])
    final_context = all_text[:3000]  # limit for speed

    if not final_context.strip():
        return BattleResponse(
            answers=["No answer found in the document."] * len(req.questions)
        )

    # 3️⃣ Combine questions
    combined_questions = "\n".join(
        f"{i+1}. {q}" for i, q in enumerate(req.questions)
    )

    # 4️⃣ Build prompt
    prompt = f"""
You are a precise assistant.
Answer each question strictly using ONLY the context below.
Do not use outside knowledge.
If the answer is not present, reply exactly:
"No answer found in the document."

Context:
{final_context}

Questions:
{combined_questions}

Provide numbered answers only.
"""

    # 5️⃣ Call model ONCE
    raw_output = ask_model(prompt).strip()

    # 🔍 Debug
    print("RAW MODEL OUTPUT:\n", raw_output)

    # 6️⃣ Parse answers robustly
    answers = []
    for line in raw_output.split("\n"):
        line = line.strip()
        match = re.match(r"^\d+\s*[\.\)\-:]\s*(.*)", line)
        if match:
            answers.append(match.group(1).strip())

    # 7️⃣ Fallback if numbering not used
    if not answers:
        blocks = raw_output.split("\n\n")
        for block in blocks:
            block = block.strip()
            if block:
                answers.append(block)

    # 8️⃣ Safety padding
    while len(answers) < len(req.questions):
        answers.append("No answer found in the document.")

    return BattleResponse(answers=answers[:len(req.questions)])


# ----------------------------
# Lambda handler (Vercel)
# ----------------------------
handler = Mangum(app)
