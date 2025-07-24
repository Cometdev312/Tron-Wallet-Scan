"""Routes for wallets module."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal import services
from app.internal.routes import wallets_router
from app.pkg.connectors.database import get_async_db
from app.pkg.models import schemas


@wallets_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Wallet],
    summary="Read all wallets with pagination.",
)
@inject
async def read_wallets(
    limit: int = 10,
    page: int = 1,
    wallet_service: services.Wallets = Depends(
        Provide[services.Services.wallets],
    ),
    session: AsyncSession = Depends(get_async_db),
):
    return await wallet_service.get_wallets(
        query=schemas.RequestWalletList(limit=limit, page=page),
        session=session,
    )


@wallets_router.post(
    "",
    response_model=schemas.ResponseWalletInfo,
    status_code=status.HTTP_201_CREATED,
    summary="Get information about a wallet.",
)
@inject
async def check_wallet_info(
    cmd: schemas.RequestWalletInfo,
    wallet_service: services.Wallets = Depends(
        Provide[services.Services.wallets],
    ),
    session: AsyncSession = Depends(get_async_db),
):
    return await wallet_service.check_wallet_info(cmd=cmd, session=session)
