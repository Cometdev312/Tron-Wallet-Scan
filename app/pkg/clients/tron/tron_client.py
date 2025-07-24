"""Tron client implementation."""

from decimal import Decimal
from tronpy import AsyncTron

__all__ = ("TronClient", )


class TronClient:
    __async_tron: AsyncTron

    def __init__(self, async_tron: AsyncTron):
        self.__async_tron = async_tron

    async def get_bandwidth(self, address: str) -> int:
        return await self.__async_tron.get_bandwidth(addr=address)

    async def get_energy(self, address: str) -> int:
        return await self.__async_tron.get_energy(address=address)

    async def get_trx_balance(self, address: str) -> Decimal:
        return await self.__async_tron.get_account_balance(addr=address)
