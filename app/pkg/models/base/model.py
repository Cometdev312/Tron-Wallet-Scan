"""Base model for all models in API server."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import UUID

import pydantic
from jsf import JSF
from pydantic import ConfigDict

__all__ = ("BaseModel", "Model")

Model = TypeVar("Model", bound="BaseModel")
_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    """Base model for all models in API server."""

    def to_dict(
        self,
        show_secrets: bool = False,
        values: dict[Any, Any] = None,
        by_alias: bool = True,
        **kwargs,
    ) -> dict[Any, Any]:
        """Make transfer model to Dict object.

        Args:
            by_alias: Whether field aliases should be used as keys in the
                returned dictionary
                Default: ``True``.
            show_secrets: Shows secret in dict object if True.
                Default: ``False``.
            values: Using an object to write to a Dict object.
                Default: ``None``.
        Keyword Args:
            Optional arguments to be passed to the Dict object.

        Returns: Dict object with reveal password filed.
        """
        values = (
            self.model_dump(by_alias=by_alias, **kwargs).items()
            if not values
            else values.items()
        )

        r = {}
        for k, v in values:
            v = self.__cast_values(
                v=v,
                show_secrets=show_secrets,
            )
            r[k] = v
        return r

    def __cast_values(
        self,
        v: _T,
        show_secrets: bool = False,
        **kwargs,
    ) -> _T:
        """Cast value for dict object.

        Args:
            v:
                Any value.
            show_secrets:
                If True, then the secret will be revealed.

        Warnings:
            This method is not memory optimized.
        """
        if isinstance(v, (List, Tuple)):
            return [
                self.__cast_values(
                    v=ve,
                    show_secrets=show_secrets,
                    **kwargs,
                )
                for ve in v
            ]

        elif isinstance(v, (pydantic.SecretBytes, pydantic.SecretStr)):
            return self.__cast_secret(
                v=v,
                show_secrets=show_secrets,
            )

        elif isinstance(v, Dict) and v:
            v = self.to_dict(show_secrets=show_secrets, values=v, **kwargs)

        elif isinstance(v, UUID):
            return str(v)

        elif isinstance(v, datetime):
            return v.timestamp()

        return v

    @staticmethod
    def __cast_secret(v, show_secrets: bool = False) -> str:
        """Cast secret value to str.

        Args:
            v: pydantic.Secret* object.
            show_secrets: bool value. If True, then the secret will be revealed.

        Returns: str value of ``v``.
        """

        if not show_secrets:
            return str(v)

        elif isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode()

        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value()

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        json_encoders={
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
        },
    )
