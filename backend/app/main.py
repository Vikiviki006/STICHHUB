"""
StitchHub — FastAPI Application Entry Point
System Architect: Claude
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base

# Create all tables on startup (use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StitchHub API",
    description="Wholesale dress catalog, fabric calculator, AR preview & shipping",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# --- Routers ---
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "stitchhub-api"}