"""
Routes untuk Core Service.

Mendefinisikan semua endpoint REST API untuk CRUD produk MongoDB.
"""

import logging
from typing import List, Dict, Any

import httpx
from fastapi import APIRouter, HTTPException

from app import mongo_service as mongo
from app.schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponse,
    ProductListResponse,
    ErrorResponse
)
from app.config import SEARCH_SERVICE_URL

logger = logging.getLogger(__name__)

router = APIRouter()


async def sinkronisasi_ke_search_service(
    method: str,
    endpoint: str,
    data: Dict[str, Any] = None
) -> None:
    """Mengirim request sinkronisasi ke Search Service.

    Args:
        method: HTTP method (POST, PUT, DELETE).
        endpoint: Endpoint path (e.g., /sync, /sync/1).
        data: Optional request body untuk POST/PUT.
    """
    url = f"{SEARCH_SERVICE_URL}/api{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            if method == "POST":
                await client.post(url, json=data)
            elif method == "PUT":
                await client.put(url, json=data)
            elif method == "DELETE":
                await client.delete(url)
        logger.info(f"Sinkronisasi berhasil: {method} {url}")
    except httpx.RequestError as e:
        logger.warning(f"Sinkronisasi gagal (Search Service mungkin offline): {e}")


@router.get("/products", response_model=ProductListResponse)
async def get_all_products():
    """Mengambil semua produk dari MongoDB."""
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        products = mongo.cari_semua()
        return ProductListResponse(
            message=f"Ditemukan {len(products)} produk",
            data=products,
            total=len(products)
        )
    except Exception as e:
        logger.error(f"Error get_all_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Mengambil satu produk berdasarkan ID.

    Args:
        product_id: ID produk yang dicari.
    """
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        product = mongo.cari_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Produk dengan ID {product_id} tidak ditemukan")

        return ProductResponse(
            message="Produk ditemukan",
            data=product
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error get_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreateSchema):
    """Membuat produk baru.

    Args:
        product: Data produk baru.
    """
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        # Cek apakah ID sudah ada
        existing = mongo.cari_by_id(product._id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Produk dengan ID {product._id} sudah ada"
            )

        produk_dict = product.model_dump(by_alias=True)
        result = mongo.insert_satu(produk_dict)
        if result is None:
            raise HTTPException(status_code=500, detail="Gagal insert produk")

        # Sinkronisasi ke Search Service
        await sinkronisasi_ke_search_service("POST", "/sync", produk_dict)

        return ProductResponse(
            message=f"Produk ID {result} berhasil dibuat",
            data=produk_dict
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error create_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdateSchema):
    """Mengupdate produk berdasarkan ID.

    Args:
        product_id: ID produk yang akan diupdate.
        product: Data yang akan diupdate (partial).
    """
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        # Cek apakah produk ada
        existing = mongo.cari_by_id(product_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Produk dengan ID {product_id} tidak ditemukan"
            )

        # Filter field yang tidak None
        data_baru = product.model_dump(exclude_none=True)
        if not data_baru:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diupdate")

        berhasil = mongo.update_data(product_id, data_baru)
        if not berhasil:
            raise HTTPException(status_code=500, detail="Gagal update produk")

        # Sinkronisasi ke Search Service
        await sinkronisasi_ke_search_service("PUT", f"/sync/{product_id}", data_baru)

        # Ambil data terbaru
        updated = mongo.cari_by_id(product_id)
        return ProductResponse(
            message=f"Produk ID {product_id} berhasil diupdate",
            data=updated
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error update_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int):
    """Menghapus produk berdasarkan ID.

    Args:
        product_id: ID produk yang akan dihapus.
    """
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        # Cek apakah produk ada
        existing = mongo.cari_by_id(product_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Produk dengan ID {product_id} tidak ditemukan"
            )

        berhasil = mongo.delete_data(product_id)
        if not berhasil:
            raise HTTPException(status_code=500, detail="Gagal hapus produk")

        # Sinkronisasi ke Search Service
        await sinkronisasi_ke_search_service("DELETE", f"/sync/{product_id}")

        return ProductResponse(
            message=f"Produk ID {product_id} berhasil dihapus",
            data=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error delete_product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/seed", response_model=ProductListResponse, status_code=201)
async def seed_products():
    """Seed dataset dari products.json ke MongoDB dan Elasticsearch.

    Mengambil data dari file products.json, insert ke MongoDB,
    lalu sinkronisasi ke Search Service.
    """
    try:
        if not mongo.cek_koneksi():
            raise HTTPException(status_code=503, detail="MongoDB tidak tersedia")

        data = mongo.muat_dataset()
        if not data:
            raise HTTPException(status_code=400, detail="Dataset kosong atau file tidak ditemukan")

        jumlah = mongo.insert_banyak(data)
        if jumlah == 0:
            raise HTTPException(status_code=500, detail="Gagal seed ke MongoDB")

        # Sinkronisasi semua data ke Search Service
        await sinkronisasi_ke_search_service("POST", "/sync", {"products": data})

        return ProductListResponse(
            message=f"Berhasil seed {jumlah} produk ke MongoDB dan Elasticsearch",
            data=data,
            total=jumlah
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error seed_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))