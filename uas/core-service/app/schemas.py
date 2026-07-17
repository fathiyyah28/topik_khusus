"""
Pydantic schemas untuk Core Service.

Mendefinisikan request/response model untuk API produk.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Schema untuk data produk."""
    id: int = Field(..., alias="_id", description="ID produk")
    nama: str = Field(..., description="Nama produk")
    kategori: str = Field(..., description="Kategori produk")
    harga: int = Field(..., ge=0, description="Harga produk dalam Rupiah")
    stok: int = Field(..., ge=0, description="Jumlah stok produk")
    spesifikasi: str = Field(..., description="Spesifikasi produk")

    class Config:
        populate_by_name = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "_id": 1,
                "nama": "Laptop Asus ROG Zephyrus G14",
                "kategori": "Laptop",
                "harga": 18999000,
                "stok": 15,
                "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
            }
        }


class ProductCreateSchema(BaseModel):
    """Schema untuk membuat produk baru."""
    id: int = Field(..., alias="_id", description="ID produk")
    nama: str = Field(..., description="Nama produk")
    kategori: str = Field(..., description="Kategori produk")
    harga: int = Field(..., ge=0, description="Harga produk dalam Rupiah")
    stok: int = Field(..., ge=0, description="Jumlah stok produk")
    spesifikasi: str = Field(..., description="Spesifikasi produk")

    class Config:
        populate_by_name = True
        from_attributes = True


class ProductUpdateSchema(BaseModel):
    """Schema untuk mengupdate produk (semua field opsional)."""
    nama: Optional[str] = Field(None, description="Nama produk")
    kategori: Optional[str] = Field(None, description="Kategori produk")
    harga: Optional[int] = Field(None, ge=0, description="Harga produk")
    stok: Optional[int] = Field(None, ge=0, description="Jumlah stok")
    spesifikasi: Optional[str] = Field(None, description="Spesifikasi produk")


class ProductResponse(BaseModel):
    """Standard response wrapper untuk data produk."""
    status: str = "success"
    message: str = ""
    data: Optional[dict] = None


class ProductListResponse(BaseModel):
    """Standard response wrapper untuk list produk."""
    status: str = "success"
    message: str = ""
    data: List[dict] = []
    total: int = 0


class ErrorResponse(BaseModel):
    """Standard error response."""
    status: str = "error"
    message: str = ""
    error_code: Optional[str] = None