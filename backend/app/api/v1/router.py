"""
StitchHub — API v1 Router
Wires all endpoint modules into one router.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, dresses, fabric, orders

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(dresses.router)
api_router.include_router(fabric.router)
api_router.include_router(orders.router)