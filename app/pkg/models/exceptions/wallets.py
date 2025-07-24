"""Exceptions for a Wallet model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = (
    "WalletNotFound",
)


class WalletNotFound(BaseAPIException):
    message = "Wallet not found."
    status_code = status.HTTP_404_NOT_FOUND
