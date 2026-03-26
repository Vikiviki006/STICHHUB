"""
StitchHub — Fabric Calculator (Story B)
Core formula: total = qty × meters_per_unit × (1 + wastage_pct / 100)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
import uuid

from app.db.session import get_db
from app.models.dress import Dress
from app.models.fabric import FabricRequirement
from app.schemas.schemas import FabricCalcRequest, FabricCalcResult, FabricCalcLineItem, FabricReqCreate
from app.api.deps import require_admin

router = APIRouter(prefix="/fabric", tags=["fabric-calculator"])


def calculate_fabric(
    dress: Dress,
    requirements: list[FabricRequirement],
    quantities: dict,          # {"S": 20, "M": 20, "L": 10}
) -> FabricCalcResult:
    """
    Pure calculation logic — kept separate for easy unit testing.
    quantities keys must match FabricRequirement.size values.
    """
    line_items = []
    summary: dict[str, Decimal] = {}

    for req in requirements:
        qty = int(quantities.get(req.size, 0))
        if qty == 0:
            continue

        wastage_factor = 1 + (req.wastage_pct / Decimal("100"))
        total = Decimal(str(qty)) * req.meters_per_unit * wastage_factor
        total = total.quantize(Decimal("0.01"))

        line_items.append(FabricCalcLineItem(
            fabric_type=req.fabric_type,
            size=req.size,
            quantity=qty,
            meters_per_unit=req.meters_per_unit,
            wastage_pct=req.wastage_pct,
            total_meters=total,
        ))

        summary[req.fabric_type] = summary.get(req.fabric_type, Decimal("0")) + total

    grand_total = sum(summary.values())

    return FabricCalcResult(
        dress_name=dress.name,
        dress_sku=dress.sku,
        line_items=line_items,
        summary={k: float(v) for k, v in summary.items()},
        grand_total_meters=grand_total,
    )


# ─── API Routes ──────────────────────────────────────────────────────────────

@router.post("/calculate", response_model=FabricCalcResult)
def run_calculation(payload: FabricCalcRequest, db: Session = Depends(get_db)):
    """
    Takes a dress ID + quantity per size, returns meters needed per fabric type.
    Example: {"dress_id": "...", "quantities": {"S": 20, "M": 20, "L": 10}}
    """
    dress = db.query(Dress).filter(Dress.id == payload.dress_id).first()
    if not dress:
        raise HTTPException(status_code=404, detail="Dress not found")

    requirements = (
        db.query(FabricRequirement)
        .filter(FabricRequirement.dress_id == payload.dress_id)
        .all()
    )
    if not requirements:
        raise HTTPException(
            status_code=422,
            detail="No fabric requirements defined for this dress. Contact admin.",
        )

    return calculate_fabric(dress, requirements, payload.quantities)


@router.post("/requirements", status_code=201)
def add_fabric_requirement(
    payload: FabricReqCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_admin),
):
    """Admin: add or update fabric requirement for a dress+size combination."""
    req = FabricRequirement(**payload.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req