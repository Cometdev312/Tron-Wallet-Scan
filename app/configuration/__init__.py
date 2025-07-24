"""Collect or build all requirements for startup server.

In this module, you can add all your middlewares, routes, dependencies,
etc.

Containers need for register all dependencies in ``FastAPI`` server. For
start building your application, you **MUST** call wire_packages.

Examples:
    When you're using containers without FastAPI::

        >>> __containers__.wire_packages()

    When you using ``FastAPI`` server, you **MUST** pass an argument
    application instance::

        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __containers__.wire_packages(app=app)
"""

from app.internal.services import Services
from app.pkg.models.core import Container, Containers

from . import _pydantic_conf

__all__ = ("__containers__", )

_ = _pydantic_conf

__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Services),
    ],
)
