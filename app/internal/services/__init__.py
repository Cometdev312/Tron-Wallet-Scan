"""Service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.services.wallets import Wallets
from app.pkg.clients import Clients
from app.pkg.settings import settings

__all__ = ("Services",)


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    repositories: Repositories = providers.Container(
        Repositories,
    )
    clients = providers.Container(Clients)

    wallets = providers.Factory(
        Wallets,
        wallet_repository=repositories.wallets,
        tron_client=clients.tron_client,
    )
