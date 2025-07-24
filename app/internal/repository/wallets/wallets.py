"""Repository for wallets."""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.internal.repository.repository import Repository
from app.pkg.models import schemas
from . import models

__all__ = ("Wallets", )


class Wallets(Repository):
    """Wallets repository implementation."""

    async def create(self, cmd: schemas.RequestWalletInfo, session: AsyncSession) -> None:
        stmt = (
            insert(models.Wallets)
            .values(
                **cmd.to_dict(),
            )
            .returning(models.Wallets)
        )

        result = await session.execute(stmt)
        print("Wallet was created", result.scalar_one())
        await session.commit()

    async def read_all(self, query: schemas.RequestWalletList, session: AsyncSession) -> List[schemas.Wallet]:
        stmt = (
            select(models.Wallets)
            .offset(query.page)
            .limit(query.limit)
        )

        result = await session.execute(stmt)
        rows = result.scalars().all()
        print(rows)

        return [schemas.Wallet(address=row.address, created_at=row.created_at) for row in rows]