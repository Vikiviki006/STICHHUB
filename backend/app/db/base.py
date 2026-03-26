from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models in env.py for Alembic instead of here to prevent circular imports.