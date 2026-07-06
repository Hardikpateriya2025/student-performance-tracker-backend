"""
Declarative Base. All models import this Base.
Also acts as the single import point so Alembic sees every model.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
