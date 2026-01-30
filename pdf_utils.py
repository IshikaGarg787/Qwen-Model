# pdf_utils.py
import requests
import tempfile
from pathlib import Path
import fitz  # PyMuPDF
from io import BytesIO


def download_pdf(url: str) -> str:
    """
    Downloads PDF from a URL to a temporary file and returns the file path
    """
    response = requests.get(url)
    response.raise_for_status()  # fail if download fails

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(response.content)
    temp_file.close()

    return temp_file.name

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text (including tables as flattened text) from PDF
    Returns a single string
    """
    doc = fitz.open(file_path)
    full_text = []

    for page in doc:
        # get page text (this includes tables in most PDFs)
        page_text = page.get_text("text")
        full_text.append(page_text)

    doc.close()
    return "\n".join(full_text)


def get_pdf_pages(pdf_url: str):
    """
    Fetch PDF from URL and return list of pages with text.
    """
    try:
        resp = requests.get(pdf_url, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch PDF: {e}")

    try:
        pdf_bytes = BytesIO(resp.content)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")

    pages = []
    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text("text")
        })

    doc.close()
    return pages

def retrieve_relevant_text(pages, question, max_pages=3):
    """
    Select relevant pages based on keyword matching.
    """
    keywords = [
        w.lower() for w in question.split()
        if len(w) > 3
    ]

    matched_pages = []

    for p in pages:
        text_lower = p["text"].lower()
        if any(k in text_lower for k in keywords):
            matched_pages.append(p["text"])

        if len(matched_pages) >= max_pages:
            break

    return "\n".join(matched_pages)
