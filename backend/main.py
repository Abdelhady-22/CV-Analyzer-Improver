"""
CV Analysis & Improvement App — FastAPI entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ensure_upload_dir
from routes import upload, analysis, download, generate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ensure_upload_dir()
    yield
    # Shutdown (nothing to clean up)


app = FastAPI(
    title="CV Analysis & Improvement API",
    description="AI-powered ATS analysis, scoring, and CV rewriting",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(download.router, prefix="/api", tags=["Download"])
app.include_router(generate.router, prefix="/api", tags=["Generate"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "cv-analysis-api"}
