# pdf_utils.py

import requests
import tempfile
import fitz  # PyMuPDF
import re
from typing import List, Dict


# ----------------------------
# Utility: clean question words
# ----------------------------
def clean_words(text: str):
    """
    Extract meaningful keywords (remove punctuation, numbers, short words)
    """
    return re.findall(r"[a-zA-Z]{4,}", text.lower())


# ----------------------------
# Download PDF (STREAMING)
# ----------------------------
import time
import requests
import tempfile

def download_pdf(url: str, retries=3) -> str:
    """
    Robust PDF downloader with retries
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/pdf",
    }

    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=30,
                stream=True,
                verify=True
            )
            response.raise_for_status()

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

            for chunk in response.iter_content(chunk_size=16384):
                if chunk:
                    temp_file.write(chunk)

            temp_file.close()
            return temp_file.name

        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2)  # wait before retry


# ----------------------------
# Extract text from PDF
# ----------------------------
def extract_text_from_pdf(file_path: str) -> List[Dict]:
    """
    Extract text page-by-page from PDF.
    Returns a list of dicts:
    [
        {"page": 1, "text": "..."},
        ...
    ]
    """
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text("text")
        })

    doc.close()
    return pages


# ----------------------------
# Retrieve relevant text
# ----------------------------
def retrieve_relevant_text(pages, question, max_pages=4):
    """
    Robust retrieval for competition PDFs.
    Always returns useful context.
    """

    q = question.lower()

    # 1️⃣ If question mentions page → return that page index directly
    page_match = re.search(r"page\s+(\d+)", q)
    if page_match:
        page_no = int(page_match.group(1))
        if 1 <= page_no <= len(pages):
            return pages[page_no - 1]["text"]

    # 2️⃣ If question mentions section → return early pages (NIST structure)
    if "section" in q:
        return "\n".join(p["text"] for p in pages[:max_pages])

    # 3️⃣ Methodology / summary / explain → early pages
    if any(x in q for x in ["summary", "methodology", "explain", "approach"]):
        return "\n".join(p["text"] for p in pages[:max_pages])

    # 4️⃣ Default fallback → first pages (ALWAYS NON-EMPTY)
    return "\n".join(p["text"] for p in pages[:max_pages])
