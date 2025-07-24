"""All repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.wallets import Wallets

__all__ = ("Repositories", )


class Repositories(containers.DeclarativeContainer):
    wallets = providers.Factory(Wallets)
