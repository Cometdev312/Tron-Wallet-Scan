"""Models of wallets object."""

from typing import List
from datetime import datetime

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = (
    "Wallet",
    "RequestWalletInfo",
    "RequestWalletList",
    "ResponseWalletInfo",
    "ResponseWalletList",
)


class WalletFields:
    """Model fields of wallet."""

    id: PositiveInt = Field(
        json_schema_extra={
            "description": "Wallet id.",
            "example": 1,
        }
    )
    address: str = Field(
        json_schema_extra={
            "description": "Wallet address.",
            "example": "TWLZf9gn2q8Hwavq3EQbqrgUUBhtLmZm13",
            "pattern": "^T[a-zA-Z0-9]{33}$",
        }
    )
    created_at: datetime = Field(
        json_schema_extra={
            "description": "Date of a wallet's creation.",
            "example": "19.01.2021",
        }
    )


class Wallet(BaseModel):
    address: str = WalletFields.address
    created_at: datetime = WalletFields.created_at


class RequestWalletInfo(BaseModel):
    address: str = WalletFields.address


class RequestWalletList(BaseModel):
    limit: int = 10
    page: int = 1


class ResponseWalletInfo(BaseModel):
    bandwidth: int
    energy: int
    trx_balance: float


class ResponseWalletList(BaseModel):
    addresses: List[Wallet]
