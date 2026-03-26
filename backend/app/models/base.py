from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic picks them up automatically
from app.models.user import User          # noqa
from app.models.dress import Dress        # noqa
from app.models.dress import DressImage   # noqa
from app.models.fabric import FabricRequirement  # noqa
from app.models.order import Order        # noqa
from app.models.order import OrderItem    # noqa