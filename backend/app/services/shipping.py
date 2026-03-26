"""
StitchHub — Shipping Service (Story E)
Abstraction layer over FedEx and DHL APIs.
Each carrier implementation is a separate function — swap or extend easily.

TODO (Sprint 5): Replace stub responses with real API calls.
FedEx docs:  https://developer.fedex.com/api/en-us/apis/ship.html
DHL docs:    https://developer.dhl.com/api-reference/dhl-express-mydhl-api
"""

import httpx
from app.core.config import settings


def create_shipment(carrier: str, order_id: str, address: dict, total_usd: float) -> dict:
    """
    Entry point — dispatches to the correct carrier.
    Returns: {"tracking_number": str, "label_url": str, "raw": dict}
    """
    if carrier == "fedex":
        return _fedex_create_shipment(order_id, address, total_usd)
    elif carrier == "dhl":
        return _dhl_create_shipment(order_id, address, total_usd)
    else:
        raise ValueError(f"Unsupported carrier: {carrier}")


def _fedex_create_shipment(order_id: str, address: dict, total_usd: float) -> dict:
    """
    FedEx Ship API v1 — Create Shipment
    POST https://apis.fedex.com/ship/v1/shipments

    TODO (Sprint 5):
    1. Get OAuth token from POST /oauth/token
    2. Build shipment payload (shipper, recipient, packages, service type)
    3. Parse masterTrackingNumber from response
    """
    # ── STUB — replace in Sprint 5 ─────────────────────────────────────────
    return {
        "tracking_number": f"FX-STUB-{order_id[:8].upper()}",
        "label_url": "https://example.com/label.pdf",
        "carrier": "fedex",
        "raw": {"stub": True},
    }

    # ── REAL IMPLEMENTATION (uncomment in Sprint 5) ─────────────────────────
    # token = _get_fedex_token()
    # payload = {
    #     "labelResponseOptions": "URL_ONLY",
    #     "requestedShipment": {
    #         "shipper": { "contact": {...}, "address": {...} },
    #         "recipients": [{ "contact": {...}, "address": address }],
    #         "serviceType": "FEDEX_INTERNATIONAL_PRIORITY",
    #         "packagingType": "YOUR_PACKAGING",
    #         "requestedPackageLineItems": [{ "weight": {"units": "KG", "value": 1} }],
    #     },
    #     "accountNumber": { "value": settings.FEDEX_ACCOUNT_NUMBER },
    # }
    # r = httpx.post(
    #     "https://apis.fedex.com/ship/v1/shipments",
    #     json=payload,
    #     headers={"Authorization": f"Bearer {token}"},
    # )
    # r.raise_for_status()
    # data = r.json()
    # tracking = data["output"]["transactionShipments"][0]["masterTrackingNumber"]
    # return {"tracking_number": tracking, "carrier": "fedex", "raw": data}


def _dhl_create_shipment(order_id: str, address: dict, total_usd: float) -> dict:
    """
    DHL Express MyDHL+ API — Create Shipment
    POST https://express.api.dhl.com/mydhlapi/shipments

    TODO (Sprint 5):
    1. Basic Auth with DHL_API_KEY + DHL_API_SECRET
    2. Build shipment payload
    3. Parse shipmentTrackingNumber from response
    """
    # ── STUB ─────────────────────────────────────────────────────────────────
    return {
        "tracking_number": f"DHL-STUB-{order_id[:8].upper()}",
        "label_url": "https://example.com/dhl-label.pdf",
        "carrier": "dhl",
        "raw": {"stub": True},
    }


def _get_fedex_token() -> str:
    """OAuth2 client credentials for FedEx."""
    r = httpx.post(
        "https://apis.fedex.com/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": settings.FEDEX_API_KEY,
            "client_secret": settings.FEDEX_SECRET_KEY,
        },
    )
    r.raise_for_status()
    return r.json()["access_token"]