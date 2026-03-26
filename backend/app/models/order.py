"""
StitchHub — Order & OrderItem Models (Story E: Shipping Integration)
"""

import uuid
import enum
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class ShippingCarrier(str, enum.Enum):
    fedex = "fedex"
    dhl = "dhl"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    total_usd = Column(Numeric(12, 2), nullable=False)
    shipping_address = Column(Text, nullable=True)           # JSON string
    shipping_carrier = Column(Enum(ShippingCarrier), nullable=True)
    tracking_number = Column(String(255), nullable=True)     # Returned by FedEx/DHL
    carrier_response = Column(Text, nullable=True)           # Full API response JSON
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shipped_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    dress_id = Column(UUID(as_uuid=True), ForeignKey("dresses.id"), nullable=False)
    quantity = Column(String(20), nullable=False)
    size = Column(String(10), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)      # Price snapshot at order time

    # Relationships
    order = relationship("Order", back_populates="items")
    dress = relationship("Dress", back_populates="order_items")