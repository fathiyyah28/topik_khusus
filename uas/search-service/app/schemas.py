"""
Pydantic schemas untuk Search Service.

Mendefinisikan request/response model untuk API pencarian.
"""

from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class SearchResponse(BaseModel):
    """Response untuk pencarian."""
    status: str = "success"
    message: str = ""
    data: List[dict] = []
    total: int = 0
    keyword: str = ""


class SyncRequest(BaseModel):
    """Request untuk sinkronisasi data.""" 
    products: Optional[List[Dict[str, Any]]] = Field(None, description="List produk untuk bulk sync")


class SyncResponse(BaseModel):
    """Response untuk sinkronisasi."""
    status: str = "success"
    message: str = ""
    total: int = 0


class StatsResponse(BaseModel):
    """Response untuk statistik index."""
    status: str = "success"
    data: dict = {}


class ErrorResponse(BaseModel):
    """Standard error response."""
    status: str = "error"
    message: str = ""
    error_code: Optional[str] = None