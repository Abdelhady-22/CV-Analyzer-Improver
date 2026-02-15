# CV Analyzer & Improver

A full-stack AI-powered CV analysis and improvement platform. Upload your CV, get instant ATS compliance scoring with explainable findings, actionable recommendations, and a rewritten improved version — or generate a brand-new ATS-optimized CV from scratch.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![CrewAI](https://img.shields.io/badge/CrewAI-FF6B35?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📄 CV Upload** | Drag-and-drop PDF/DOCX upload with validation (size & page limits) |
| **🔍 ATS Analysis** | 5-agent CrewAI pipeline: Infer → Analyze → Score → Recommend → Rewrite |
| **📊 Hybrid Scoring** | 60% deterministic rules (explainable) + 40% AI quality judgment |
| **💡 Recommendations** | Actionable edits with before/after text and clear rationale |
| **✏️ Auto-Rewrite** | Surgical paragraph-level edits applied directly to your DOCX |
| **📝 Diff Viewer** | Inline before/after comparison of original vs improved CV |
| **🚀 CV Generator** | Multi-step form to build a new ATS-safe CV from structured data |
| **🎯 Job Targeting** | Optional job title + description for keyword relevance matching |
| **⚡ Pipeline Progress** | Real-time per-agent progress indicator with polling |
| **💾 Persistence** | Supabase for uploads and analysis result caching |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    React Frontend                   │
│  Upload → Analysis Dashboard → Generate CV          │
│  (Zustand · React Router · Vite · TypeScript)       │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                     │
│  Routes → Services → CrewAI Agents → Repositories   │
├─────────────────────────────────────────────────────┤
│  Agents: Infer · Analyze · Score · Recommend · Rew. │
│  LLM:    Ollama (default) | Gemini | OpenAI         │
│  DB:     Supabase (uploads + analyses)              │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
devops-project/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Centralized settings
│   ├── models/                 # Pydantic schemas
│   ├── repositories/           # Supabase data layer
│   ├── services/               # Business logic (parser, scoring, editor, generator, diff)
│   ├── agents/                 # CrewAI agents + crew orchestrator
│   └── routes/                 # API endpoints
├── frontend/
│   └── src/
│       ├── models/types.ts     # TypeScript interfaces
│       ├── services/api.ts     # API client
│       ├── store/              # Zustand state management
│       ├── components/         # 11 UI components
│       └── routes/             # 3 page routes
├── README.md
├── QUICKSTART.md
└── LICENSE
```

---

## 🔧 Tech Stack

### Backend
- **FastAPI** — async REST API with background tasks
- **CrewAI** — multi-agent AI orchestration
- **LiteLLM** — unified LLM interface (Ollama / Gemini / OpenAI)
- **python-docx** — DOCX reading, editing, and generation
- **pdfplumber** — PDF text extraction
- **Supabase** — PostgreSQL database
- **diff-match-patch** — text diff computation

### Frontend
- **React 19** + **TypeScript** — type-safe UI
- **Vite** — fast dev server and build
- **Zustand** — lightweight state management
- **React Router** — client-side routing

---

## ⚙️ Configuration

All config is via `.env` in the `backend/` directory:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `ollama` | `ollama`, `gemini`, or `openai` |
| `LLM_MODEL` | `llama3.1` | Model name for the chosen provider |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `GEMINI_API_KEY` | — | Required if provider is `gemini` |
| `OPENAI_API_KEY` | — | Required if provider is `openai` |
| `SUPABASE_URL` | — | Supabase project URL |
| `SUPABASE_KEY` | — | Supabase anon/service key |
| `MAX_FILE_SIZE_MB` | `10` | Max upload file size |
| `MAX_PAGE_COUNT` | `20` | Max CV page count |

---

## 🛣️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload PDF/DOCX |
| `POST` | `/api/analyze` | Start analysis pipeline |
| `GET` | `/api/analyze/status/{id}` | Poll pipeline progress |
| `GET` | `/api/analyze/result/{id}` | Get cached results |
| `GET` | `/api/download/{id}` | Download improved CV |
| `GET` | `/api/download/original/{id}` | Download original CV |
| `POST` | `/api/generate` | Generate new CV from data |
| `GET` | `/api/generate/download/{id}` | Download generated CV |
| `GET` | `/health` | Health check |

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
