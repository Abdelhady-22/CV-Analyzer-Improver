# CV Analyzer & Improver

A full-stack AI-powered CV analysis and improvement platform. Upload your CV, get instant ATS compliance scoring with explainable findings, actionable recommendations, and a rewritten improved version — or generate a brand-new ATS-optimized CV from scratch.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![CrewAI](https://img.shields.io/badge/CrewAI-FF6B35?style=for-the-badge)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

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
CV-Analyzer-Improver/
├── docker-compose.yml          # Docker orchestration
├── backend/
│   ├── Dockerfile              # Backend container
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Centralized settings
│   ├── .env.example            # Environment template
│   ├── models/                 # Pydantic schemas
│   ├── repositories/           # Supabase data layer
│   ├── services/               # Business logic
│   ├── agents/                 # CrewAI agents + orchestrator
│   └── routes/                 # API endpoints
├── frontend/
│   ├── Dockerfile              # Frontend container
│   ├── nginx.conf              # Nginx reverse proxy config
│   └── src/
│       ├── models/types.ts     # TypeScript interfaces
│       ├── services/api.ts     # API client
│       ├── store/              # Zustand state management
│       ├── components/         # UI components
│       └── routes/             # Page routes
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

### DevOps
- **Docker** + **Docker Compose** — containerized deployment
- **Nginx** — reverse proxy and static file serving

---

## ⚙️ Configuration

Copy the template and fill in your values:

```bash
cp backend/.env.example backend/.env
```

Available variables in `backend/.env`:

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

## 🐳 Docker Deployment

```bash
# 1. Start Ollama on your host machine
ollama serve

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your Supabase credentials

# 3. Build and start all containers
docker compose up --build

# 4. Open the app
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# Health:   http://localhost:8000/health
```

Useful commands:

```bash
docker compose up -d             # Run in background
docker compose logs -f backend   # Tail backend logs
docker compose down              # Stop all containers
```

> **Note:** Ollama runs on your host machine, not in Docker. The backend container connects to it via `host.docker.internal`.

---

## 🚀 Getting Started (Local)

See [QUICKSTART.md](QUICKSTART.md) for local development setup without Docker.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
