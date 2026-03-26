"""
StitchHub — FabricRequirement Model (Story B: Fabric Calculator)
Stores fabric per dress+size, used by the calculator service.
"""

import uuid
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class FabricRequirement(Base):
    __tablename__ = "fabric_requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dress_id = Column(UUID(as_uuid=True), ForeignKey("dresses.id", ondelete="CASCADE"), nullable=False)
    size = Column(String(10), nullable=False)                # XS / S / M / L / XL
    fabric_type = Column(String(100), nullable=False)        # e.g. "silk", "chiffon", "cotton"
    meters_per_unit = Column(Numeric(6, 3), nullable=False)  # base yardage for 1 dress
    wastage_pct = Column(Numeric(5, 2), default=10.0)        # % wastage (default 10%)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    dress = relationship("Dress", back_populates="fabric_requirements")