from fastapi import FastAPI
from mangum import Mangum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from pdf_utils import get_pdf_pages, retrieve_relevant_text
from prompt import build_prompt
from model_runner import ask_model
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for competition)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="AI Battle Arena")


class BattleRequest(BaseModel):
    pdf_url: str
    questions: List[str]


class BattleResponse(BaseModel):
    answers: List[str]


@app.post("/aibattle", response_model=BattleResponse)
def aibattle(req: BattleRequest):
    try:
        # 1️⃣ Load PDF pages
        pages = get_pdf_pages(req.pdf_url)

        answers = []

        # 2️⃣ Answer each question
        for q in req.questions:
            context = retrieve_relevant_text(pages, q)

            # If nothing relevant found → safe abstain
            if not context.strip():
                answers.append("No answer found in the document.")
                continue

            prompt = build_prompt(context, q)
            answer = ask_model(prompt).strip()

            # Final safety check
            if not answer:
                answers.append("No answer found in the document.")
            else:
                answers.append(answer.rstrip(".") + ".")

        return BattleResponse(answers=answers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)