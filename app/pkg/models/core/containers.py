"""Models for dependency_injector containers."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Union, Type

from dependency_injector.containers import Container as _DIContainer
from dependency_injector import containers
from fastapi import FastAPI
from pydantic import StrictStr

from app.pkg.models.core.meta import SingletonMeta

__all__ = ("Container", "Containers")


@dataclass(frozen=True)
class Container:
    """Model for contain single container.

    Attributes:
        container:
            dependency_injector declarative container callable object.
        packages:
            Array of packages to which the injector will be available.
            Default: ["app"]
    """

    container: Union[Callable[..., containers.Container]]

    packages: List[str] = field(default_factory=lambda: ["app"])


class WiredContainer(dict, metaclass=SingletonMeta):
    """Singleton container for store all wired containers."""

    def __getitem__(self, item: object):
        """Get container by name.

        Args:
            item: Container object.

        Examples:
            ::

                >>> from app import __containers__
                >>> from app.pkg.connectors import PostgresSQL

                >>> __containers__.wire_packages(pkg_name=__name__)
                >>> __containers__.wired_containers[PostgresSQL]

        Returns:
            Container instance.
        """

        return super().__getitem__(item.__name__)


@dataclass(frozen=True)
class Containers:
    """Frozen dataclass model, for contains all declarative containers."""

    #: str: __name__ of the main package.
    pkg_name: str

    #: List[Container]: List of `Container` model.
    containers: List[Container]

    #: List[_Container]: List of instance dependency_injector containers.
    __wired_containers__: WiredContainer = field(
        init=False,
        default_factory=WiredContainer,
    )

    def wire_packages(
        self,
        app: Optional[FastAPI] = None,
        pkg_name: Optional[str] = None,
        unwire: bool = False,
    ):
        """Wire packages to the declarative containers.

        Args:
            app:
                Optional ``FastAPI`` instance.
                If passed, the containers will be written to the application context.
            pkg_name:
                Optional ``__name__`` of running module.
            unwire:
                Optional bool parameter. If `True`, un wiring all containers.

        Notes:
            If you want to use the injector in other modules, you need to set
            ``pkg_name`` parameter to the name of the module in which the injector
            is running.
            For example, you have module tree like::

                ProjectName
                ├── app
                │    ├── api
                │    │   ├── endpoints
                │    │   │   └── users.py
                │    │   └── __init__.py
                │    ├── internal
                │    │   ├── repository
                │    │   │   └── postgresql
                │    │   └── __init__.py
                │    ├── pkg
                │    │   ├── connectors
                │    │   │   └── postgresql
                │    │   └── __init__.py
                │
                └── tests
                    ├── api
                    │   ├── endpoints
                    │   │   └── users.py
                    ...

            If you want to use the injector in ``users.py`` endpoints, you need to
            set ``pkg_name="app.api.endpoints"`` in ``wire_packages`` method.
            But you also can set ``pkg_name="app"`` for use injector in all modules
            in the project (expect tests).
            And you can set ``pkg_name="tests"`` for use injector in all modules
            in the project (with tests).

        Returns:
            None
        """
        pkg_name = pkg_name if pkg_name else self.pkg_name
        for container in self.containers:
            self.__wire(container, unwire, pkg_name, app)

    def __wire(
        self,
        container: Container,
        unwire: bool,
        pkg_name: str,
        app: Optional[FastAPI] = None,
    ) -> Container:
        """Wire container to the declarative containers.

        Args:
            container: Container or Resource model.
            unwire: Optional bool parameter. If `True`, un wiring all containers.
            pkg_name: Optional __name__ of running module.
            app: Optional ``FastAPI`` instance.
                if passed, the containers will be written to the application context.

        Returns:
            ``Container``
        """

        cont = container.container()

        if unwire:
            cont.unwire()
            return cont

        cont.wire(packages=[pkg_name, *container.packages])

        container_name = container.container.__name__

        if not self.__wired_containers__.get(container_name, None):
            self.__wired_containers__[container_name] = cont

        if app:
            setattr(app, container_name.lower(), cont)

        return cont
