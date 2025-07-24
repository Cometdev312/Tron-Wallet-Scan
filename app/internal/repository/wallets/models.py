"""Wallet models."""

from sqlalchemy import Column, String, Integer, DateTime, func

from app.pkg.connectors.database import Base

__all__ = ("Wallets", )


class Wallets(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
