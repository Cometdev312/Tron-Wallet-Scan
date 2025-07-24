"""All clients are defined here."""

from dependency_injector import containers, providers
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from app.pkg.clients.tron.tron_client import TronClient
from app.pkg.settings import settings


__all__ = ("Clients", )


class Clients(containers.DeclarativeContainer):
    """Declarative container with clients."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    async_tron_provider = providers.Singleton(
        AsyncHTTPProvider,
        api_key=configuration.TRON_NODE_API_KEY.get_secret_value(),
    )
    if settings.DEBUG:
        async_tron = providers.Singleton(
            AsyncTron,
            network='nile'
        )
    else:
        async_tron = providers.Singleton(
            AsyncTron,
            provider=async_tron_provider,
        )

    tron_client = providers.Factory(
        TronClient,
        async_tron=async_tron,
    )
