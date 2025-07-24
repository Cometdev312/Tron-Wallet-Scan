"""Global point for collected routers."""

from fastapi import APIRouter

from app.internal.pkg.models import Routes
from app.pkg.models.exceptions import wallets

__all__ = ("__routes__", "wallets_router")


wallets_router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
    responses={
        **wallets.WalletNotFound.generate_openapi(),
    },
)


__routes__ = Routes(
    routers=(wallets_router,),
)
