"""Server configuration."""

from typing import TypeVar
from fastapi import FastAPI

from app.internal.pkg.middlewares.handle_http_exceptions import (
    handle_api_exceptions,
    handle_internal_exception,
)
from app.internal.routes import __routes__
from app.pkg.models.base import BaseAPIException

__all__ = ("Server", )


FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class Server:
    """Register all requirements for correct work of server instance."""

    def __init__(self, app: FastAPI):
        self.__app = app
        self._register_routes(app)
        self._register_http_exceptions(app)

    def get_app(self) -> FastAPIInstance:
        """Get current application instance.

        Returns: ``FastAPI`` application instance.
        """
        return self.__app

    @staticmethod
    def _register_routes(app: FastAPIInstance) -> None:
        """Include routers in ``FastAPI`` instance from ``__routes__``.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        __routes__.allocate_routes(app)

    @staticmethod
    def _register_http_exceptions(app: FastAPIInstance) -> None:
        """Register http exceptions.

        FastAPIInstance handle BaseApiExceptions raises inside functions.

        Args:
            app: ``FastAPI`` application instance

        Returns: None
        """

        app.add_exception_handler(BaseAPIException, handle_api_exceptions)
        app.add_exception_handler(Exception, handle_internal_exception)
