"""
StitchHub — Pydantic Schemas (Request / Response DTOs)
"""

from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from enum import Enum


# ─── Auth ────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    company_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str


class UserOut(BaseModel):
    id: UUID4
    email: EmailStr
    full_name: str
    company_name: Optional[str]
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Dress ───────────────────────────────────────────────────────────────────

class DressImageOut(BaseModel):
    id: UUID4
    url: str
    angle: str
    is_primary: bool

    class Config:
        from_attributes = True


class DressCreate(BaseModel):
    name: str
    sku: str
    category: str
    description: Optional[str] = None
    price_usd: Decimal
    min_order_qty: str = "10"
    available_sizes: str = "XS,S,M,L,XL"
    available_colors: Optional[str] = None
    model_3d_url: Optional[str] = None


class DressOut(BaseModel):
    id: UUID4
    name: str
    sku: str
    category: str
    description: Optional[str]
    price_usd: Decimal
    min_order_qty: str
    available_sizes: str
    model_3d_url: Optional[str]
    images: List[DressImageOut] = []
    created_at: datetime

    class Config:
        from_attributes = True


class DressListOut(BaseModel):
    items: List[DressOut]
    total: int
    page: int
    page_size: int


# ─── Fabric Calculator ────────────────────────────────────────────────────────

class FabricReqCreate(BaseModel):
    dress_id: UUID4
    size: str
    fabric_type: str
    meters_per_unit: Decimal
    wastage_pct: Decimal = Decimal("10.0")
    notes: Optional[str] = None


class FabricCalcRequest(BaseModel):
    dress_id: UUID4
    quantities: dict  # e.g. {"S": 20, "M": 20, "L": 10}


class FabricCalcLineItem(BaseModel):
    fabric_type: str
    size: str
    quantity: int
    meters_per_unit: Decimal
    wastage_pct: Decimal
    total_meters: Decimal


class FabricCalcResult(BaseModel):
    dress_name: str
    dress_sku: str
    line_items: List[FabricCalcLineItem]
    summary: dict                    # {"silk": 45.5, "lining": 30.0}
    grand_total_meters: Decimal


# ─── Orders ──────────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    dress_id: UUID4
    quantity: int
    size: str


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: dict
    shipping_carrier: str = "fedex"
    notes: Optional[str] = None


class OrderItemOut(BaseModel):
    id: UUID4
    dress_id: UUID4
    quantity: str
    size: str
    unit_price: Decimal

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: UUID4
    status: str
    total_usd: Decimal
    shipping_carrier: Optional[str]
    tracking_number: Optional[str]
    items: List[OrderItemOut] = []
    created_at: datetime

    class Config:
        from_attributes = True