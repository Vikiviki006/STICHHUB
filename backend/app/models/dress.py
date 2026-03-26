"""
StitchHub — Dress & DressImage Models (Story A: Catalog, Story D: AR)
"""

import uuid
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Dress(Base):
    __tablename__ = "dresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)          # bridal, casual, evening, etc.
    description = Column(Text, nullable=True)
    price_usd = Column(Numeric(10, 2), nullable=False)
    min_order_qty = Column(String(20), default="10")
    available_sizes = Column(String(100), default="XS,S,M,L,XL")  # CSV
    available_colors = Column(Text, nullable=True)           # JSON string
    model_3d_url = Column(Text, nullable=True)               # S3 path to .glb file (Story D)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    images = relationship("DressImage", back_populates="dress", cascade="all, delete-orphan")
    fabric_requirements = relationship("FabricRequirement", back_populates="dress", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="dress")


class DressImage(Base):
    __tablename__ = "dress_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dress_id = Column(UUID(as_uuid=True), ForeignKey("dresses.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)                       # S3 presigned URL
    angle = Column(String(50), default="front")              # front / back / side / detail
    is_primary = Column(Boolean, default=False)
    sort_order = Column(String(10), default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    dress = relationship("Dress", back_populates="images")