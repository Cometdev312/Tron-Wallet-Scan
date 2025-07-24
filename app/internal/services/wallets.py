"""Service for manage wallets."""

import asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.exceptions import BadAddress

from app.internal import repository
from app.internal.repository.repository import BaseRepository
from app.pkg.clients.tron.tron_client import TronClient
from app.pkg.models import schemas
from app.pkg.models.exceptions.wallets import WalletNotFound

__all__ = ("Wallets", )


class Wallets:
    """Service for manage wallets."""

    __wallet_repository: repository.Wallets
    __tron_client: TronClient

    def __init__(
        self,
        wallet_repository: BaseRepository,
        tron_client: TronClient,
    ):
        self.__wallet_repository = wallet_repository
        self.__tron_client = tron_client

    async def get_wallets(
        self,
        query: schemas.RequestWalletList,
        session: AsyncSession,
    ) -> List[schemas.Wallet]:
        return await self.__wallet_repository.read_all(query=query, session=session)

    async def check_wallet_info(
        self,
        cmd: schemas.RequestWalletInfo,
        session: AsyncSession,
    ) -> schemas.ResponseWalletInfo:

        tasks = (
            asyncio.create_task(task) for task in (
                self.__tron_client.get_energy(address=cmd.address),
                self.__tron_client.get_bandwidth(address=cmd.address),
                self.__tron_client.get_trx_balance(address=cmd.address),
            )
        )

        try:
            energy, bandwidth, trx_balance = await asyncio.gather(*tasks)
        except BadAddress as e:
            raise WalletNotFound from e
        else:
            await self.__wallet_repository.create(cmd=cmd, session=session)

            return schemas.ResponseWalletInfo(
                energy=energy,
                bandwidth=bandwidth,
                trx_balance=trx_balance,
            )
