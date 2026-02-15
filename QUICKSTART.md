# Quick Start Guide

Get the CV Analyzer & Improver running in under 5 minutes.

---

## Prerequisites

- **Ollama** running locally (or Gemini/OpenAI API key)
- **Supabase** project (free tier works)
- **Docker** + **Docker Compose** (recommended) — OR Python 3.10+ and Node.js 18+

---

## 1. Clone & Configure

```bash
git clone https://github.com/Abdelhady-22/CV-Analyzer-and-Improver.git
cd CV-Analyzer-and-Improver
```

Copy the environment template and fill in your credentials:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` — set your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

> **💡 Tip:** See `.env.example` for all available options (LLM provider, model, upload limits).

---

## 2. Supabase Tables

Create these tables in your Supabase dashboard (**SQL Editor → New query → Run**):

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
  upload_id UUID REFERENCES uploads(id) ON DELETE CASCADE,
  result JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_analyses_upload_id ON analyses(upload_id);

-- Enable Row Level Security
ALTER TABLE public.uploads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all access" ON public.uploads FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all access" ON public.analyses FOR ALL USING (true) WITH CHECK (true);
```

> **New to Supabase?** Sign up free at [supabase.com](https://supabase.com), create a project, then use the SQL Editor to run the above.

---

## 3. Start the App

### Option A: Docker (Recommended)

```bash
# Start Ollama on your host machine
ollama serve

# Build and launch all containers
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **Health:** http://localhost:8000/health

```bash
# Useful commands
docker compose up -d             # Run in background
docker compose logs -f backend   # Tail backend logs
docker compose down              # Stop all containers
```

> **Note:** Ollama runs on your host machine. The backend container connects to it automatically via `host.docker.internal`.

### Option B: Local Development

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000

---

## 4. Use the App

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

Restart the backend (or `docker compose restart backend`) after changing provider settings.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `CORS error` in browser | Ensure correct ports: 5173 (local) or 3000 (Docker) |
| `Ollama connection refused` | Start Ollama: `ollama serve` then `ollama pull llama3.1` |
| `Upload fails (413)` | File exceeds `MAX_FILE_SIZE_MB` (default 10 MB) |
| `Analysis stuck` | Check backend logs for LLM timeout; try a smaller model |
| `Supabase tables empty` | Verify `SUPABASE_URL` uses the REST URL (`https://...supabase.co`), not the PostgreSQL connection string |
| `RLS Disabled` warning | Run the RLS SQL commands from step 2 in Supabase SQL Editor |
| Docker: `container can't reach Ollama` | Ensure Ollama is running on host and `extra_hosts` is set in `docker-compose.yml` |

