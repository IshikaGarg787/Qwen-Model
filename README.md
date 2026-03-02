<h1>🧠 AI Battle Arena – PDF Question Answering (Qwen)</h1>

This project implements a /aibattle API that answers questions strictly based on the content of a provided PDF link using Qwen2.5 running locally via Ollama.

No external LLM APIs or Hugging Face services are used.

<h2>🚀 How It Works</h2>

Client sends a PDF URL and question to /aibattle

Server downloads the PDF

Extracts text from the document

Sends extracted content + question to Qwen

Returns answer based only on that PDF

<h2>📄 API Usage</h2>
Endpoint
POST /aibattle
Example Request
{
  "pdf_url": "https://example.com/sample.pdf",
  "question": "Summarize the key points."
}
<h2>▶️ Run Locally</h2>

Pull model:

ollama pull qwen2.5:3b

Start server:

uvicorn main:app --reload
<h2>🌍 Public Deployment (ngrok Free Tier)</h2>
ngrok http 8000

Use generated public URL:

https://your-id.ngrok-free.app/aibattle
<h2>✅ Compliance</h2>

Uses approved pretrained model (Qwen)

Fully local inference via Ollama

Required /aibattle endpoint implemented

Answers generated strictly from provided PDF content
