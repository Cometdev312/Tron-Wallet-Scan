import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dependency_injector.wiring import inject, Provide

from app.internal import services
from app.internal.repository.wallets.models import Wallets
from app.pkg.models import schemas
from app.pkg.models.exceptions.wallets import WalletNotFound


@pytest.mark.asyncio(loop_scope="session")
@inject
async def test_check_wallet_info(
    db_session: AsyncSession,
    wallet_service: services.Wallets = Provide[services.Services.wallets],
):
    wallet_info = await wallet_service.check_wallet_info(
        cmd=schemas.RequestWalletInfo(address="TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi"),
        session=db_session
    )

    assert wallet_info.trx_balance > 0  # wallet is activated

    fetched_wallet = (
        await db_session.execute(
            select(Wallets).filter(Wallets.address == "TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi")
        )
    ).scalar()

    assert fetched_wallet is not None


@pytest.mark.asyncio(loop_scope="session")
@inject
async def test_wallet_not_found(
    db_session: AsyncSession,
    wallet_service: services.Wallets = Provide[services.Services.wallets],
):
    with pytest.raises(WalletNotFound):
        await wallet_service.check_wallet_info(
            cmd=schemas.RequestWalletInfo(address="1VF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi"),  # bad address
            session=db_session
        )

    fetched_wallet = (
        await db_session.execute(
            select(Wallets).filter(Wallets.address == "1VF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi")
        )
    ).scalar()

    assert fetched_wallet is None
