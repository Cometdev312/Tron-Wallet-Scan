import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.repository.wallets.models import Wallets


@pytest.mark.asyncio(loop_scope="session")
async def test_wallet_creation(db_session: AsyncSession):
    wallet = Wallets(address="TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi")
    db_session.add(wallet)
    await db_session.commit()

    fetched_wallet = (await db_session.execute(select(Wallets))).scalar()
    assert fetched_wallet.address == "TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi"
