# Quick Start Guide

Get the CV Analyzer & Improver running locally in under 5 minutes.

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**
- **Ollama** running locally (or Gemini/OpenAI API key)
- **Supabase** project (free tier works)

---

## 1. Clone & Configure

```bash
git clone https://github.com/Abdelhady-22/CV-Analyzer-and-Improver.git
cd CV-Analyzer-and-Improver
```

Edit `backend/.env` with your credentials:

```env
# LLM — pick one provider
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

---

## 2. Supabase Tables

Create these tables in your Supabase dashboard (SQL Editor):

```sql
CREATE TABLE uploads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  filename TEXT NOT NULL,
  original_path TEXT NOT NULL,
  improved_path TEXT,
  status TEXT DEFAULT 'uploaded',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  upload_id UUID REFERENCES uploads(id),
  result JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## 3. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Verify: open http://localhost:8000/health — should return `{"status": "ok"}`.

---

## 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

---

## 5. Use the App

1. **Upload** — drag-and-drop a PDF or DOCX CV
2. **Analyze** — click "Analyze CV" (optionally set a target job)
3. **Review** — see ATS score, issues, and recommendations
4. **Download** — get the improved DOCX
5. **Generate** — or build a new CV from scratch via the form

---

## Using Gemini or OpenAI Instead of Ollama

Edit `backend/.env`:

```env
# Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your-api-key

# Or OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-api-key
```

Restart the backend after changing provider settings.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `CORS error` in browser | Ensure backend runs on port 8000 and frontend on 5173 |
| `Ollama connection refused` | Start Ollama: `ollama serve` then `ollama pull llama3.1` |
| `Upload fails (413)` | File exceeds `MAX_FILE_SIZE_MB` (default 10 MB) |
| `Analysis stuck` | Check backend logs for LLM timeout; try a smaller model |
