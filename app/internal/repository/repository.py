"""Base Repository."""

from abc import ABC
from typing import List, TypeVar, Optional

from app.pkg.models.base import Model

__all__ = ("Repository", "BaseRepository")


BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Base repository interface."""

    async def create(self, cmd: Model, *args, **kwargs) -> Model:
        raise NotImplementedError

    async def read(self, query: Model, *args, **kwargs) -> Model:
        raise NotImplementedError

    async def read_all(self, query: Optional[Model], *args, **kwargs) -> List[Model]:
        raise NotImplementedError

    async def update(self, cmd: Model, *args, **kwargs) -> Model:
        raise NotImplementedError

    async def delete(self, cmd: Model, *args, **kwargs) -> Model:
        raise NotImplementedError
