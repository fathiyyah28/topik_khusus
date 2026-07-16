"""
Routes untuk Search Service.

Mendefinisikan endpoint REST API untuk pencarian Elasticsearch
dan sinkronisasi data dari Core Service.
"""

import logging
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, Query

from app import elastic_service as es
from app.schemas import (
    SearchResponse,
    SyncRequest,
    SyncResponse,
    StatsResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search_products(
    q: str = Query(..., min_length=1, description="Kata kunci pencarian")
):
    """Mencari produk menggunakan full-text search Elasticsearch.

    Args:
        q: Kata kunci pencarian (minimal 1 karakter).
    """
    try:
        if not es.cek_koneksi():
            raise HTTPException(
                status_code=503,
                detail="Elasticsearch tidak tersedia"
            )

        hasil = es.cari_match(q)
        return SearchResponse(
            message=f"Ditemukan {len(hasil)} hasil untuk '{q}'",
            data=hasil,
            total=len(hasil),
            keyword=q
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error search_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync", response_model=SyncResponse, status_code=201)
async def sync_products(request: SyncRequest):
    """Sinkronisasi data dari Core Service ke Elasticsearch.

    Menerima list produk dan mengindexnya ke Elasticsearch.
    Digunakan oleh Core Service saat seed data.

    Args:
        request: Request body berisi list produk.
    """
    try:
        if not es.cek_koneksi():
            raise HTTPException(
                status_code=503,
                detail="Elasticsearch tidak tersedia"
            )

        if not request.products:
            raise HTTPException(
                status_code=400,
                detail="Tidak ada data produk untuk disinkronisasi"
            )

        jumlah = es.index_banyak(request.products)
        return SyncResponse(
            message=f"Berhasil sinkronisasi {jumlah} produk ke Elasticsearch",
            total=jumlah
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sync_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/sync/{product_id}", response_model=SyncResponse)
async def sync_update_product(product_id: int, data: Dict[str, Any]):
    """Update single document di Elasticsearch.

    Dipanggil oleh Core Service saat produk diupdate.

    Args:
        product_id: ID produk yang diupdate.
        data: Data yang diupdate (partial).
    """
    try:
        if not es.cek_koneksi():
            raise HTTPException(
                status_code=503,
                detail="Elasticsearch tidak tersedia"
            )

        if not data:
            raise HTTPException(
                status_code=400,
                detail="Tidak ada data untuk diupdate"
            )

        berhasil = es.update_data(product_id, data)
        if not berhasil:
            raise HTTPException(
                status_code=404,
                detail=f"Produk ID {product_id} tidak ditemukan di Elasticsearch"
            )

        return SyncResponse(
            message=f"Produk ID {product_id} berhasil diupdate di Elasticsearch",
            total=1
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sync_update_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sync/{product_id}", response_model=SyncResponse)
async def sync_delete_product(product_id: int):
    """Hapus document dari Elasticsearch.

    Dipanggil oleh Core Service saat produk dihapus.

    Args:
        product_id: ID produk yang dihapus.
    """
    try:
        if not es.cek_koneksi():
            raise HTTPException(
                status_code=503,
                detail="Elasticsearch tidak tersedia"
            )

        berhasil = es.delete_data(product_id)
        if not berhasil:
            raise HTTPException(
                status_code=404,
                detail=f"Produk ID {product_id} tidak ditemukan di Elasticsearch"
            )

        return SyncResponse(
            message=f"Produk ID {product_id} berhasil dihapus dari Elasticsearch",
            total=1
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sync_delete_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_search_stats():
    """Mendapatkan statistik index Elasticsearch.

    Returns:
        Informasi jumlah dokumen, ukuran index, dll.
    """
    try:
        stats = es.dapatkan_stats()
        return StatsResponse(
            data=stats
        )
    except Exception as e:
        logger.error(f"Error get_search_stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))