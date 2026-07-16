"""
Main entry point untuk Core Service.

Menjalankan FastAPI server untuk CRUD produk MongoDB.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.config import HOST, PORT

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- FASTAPI APP ---
app = FastAPI(
    title="Core Service - Toko Komputer",
    description="REST API untuk CRUD produk MongoDB. "
                "Bagian dari aplikasi demonstrasi MongoDB + Elasticsearch.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "service": "Core Service",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


def main():
    """Menjalankan server FastAPI dengan uvicorn."""
    import uvicorn
    logger.info(f"Core Service starting on {HOST}:{PORT}")
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=True
    )


if __name__ == "__main__":
    main()