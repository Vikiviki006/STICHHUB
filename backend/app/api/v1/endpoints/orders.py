"""
StitchHub — Orders & Shipping Endpoints (Story E)
POST /orders          — create order
GET  /orders          — list my orders
GET  /orders/{id}     — order detail
POST /orders/{id}/ship — trigger FedEx/DHL shipment
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from decimal import Decimal
import uuid

from app.db.session import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.dress import Dress
from app.models.user import User
from app.schemas.schemas import OrderCreate, OrderOut
from app.api.deps import get_current_user, require_wholesaler
from app.services.shipping import create_shipment

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_wholesaler),
):
    # Build line items + calculate total
    items = []
    total = Decimal("0")
    for item_in in payload.items:
        dress = db.query(Dress).filter(Dress.id == item_in.dress_id, Dress.is_active == True).first()
        if not dress:
            raise HTTPException(status_code=404, detail=f"Dress {item_in.dress_id} not found")
        line_total = dress.price_usd * item_in.quantity
        total += line_total
        items.append(OrderItem(
            dress_id=dress.id,
            quantity=str(item_in.quantity),
            size=item_in.size,
            unit_price=dress.price_usd,
        ))

    import json
    order = Order(
        user_id=current_user.id,
        total_usd=total,
        shipping_address=json.dumps(payload.shipping_address),
        shipping_carrier=payload.shipping_carrier,
        notes=payload.notes,
        items=items,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_wholesaler),
):
    return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_wholesaler),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/{order_id}/ship", response_model=OrderOut)
def ship_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_wholesaler),
):
    """
    Triggers FedEx or DHL shipment creation.
    Returns order with tracking_number populated.
    """
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != OrderStatus.confirmed:
        raise HTTPException(status_code=400, detail="Order must be confirmed before shipping")

    import json
    address = json.loads(order.shipping_address or "{}")
    tracking = create_shipment(
        carrier=order.shipping_carrier,
        order_id=str(order.id),
        address=address,
        total_usd=float(order.total_usd),
    )

    order.tracking_number = tracking["tracking_number"]
    order.status = OrderStatus.shipped
    db.commit()
    db.refresh(order)
    return order