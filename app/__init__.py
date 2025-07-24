"""Main factory builder of ``FastAPI`` server."""

from fastapi import Depends, FastAPI

from app.configuration import __containers__
from app.configuration.server import Server
from app.internal.pkg.middlewares.x_auth_token import get_x_token_key

__all__ = ("create_app", )


def create_app() -> FastAPI:
    app = FastAPI(dependencies=[Depends(get_x_token_key)])
    __containers__.wire_packages(app=app)
    return Server(app).get_app()
