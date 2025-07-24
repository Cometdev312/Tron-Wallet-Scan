"""Base exception for API."""

from starlette import status

__all__ = ("BaseAPIException", )


class BaseAPIException(Exception):
    """Base internal API Exception.

    Attributes:
        message:
            Message of exception.
        status_code:
            Status code of exception.

    Examples:
        Before using this class, you must create your own exception class.
        And inherit from this class.::

            >>> from app.pkg.models.base.exception import BaseAPIException
            >>> from starlette import status
            >>> class MyException(BaseAPIException):
            ...     message = "My exception"
            ...     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        After that, you can use it in your code in some function run under fastapi::

            >>> async def my_func():
            ...     raise MyException
    """

    #: str: Human readable string describing the exception.
    message: str = "Base API Exception"
    #: int: Exception error code.
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    @classmethod
    def generate_openapi(cls):
        return {
            cls.status_code: {
                "description": cls.message,
                "content": {
                    "application/json": {
                        "example": {
                            "message": cls.message,
                        },
                    },
                },
            },
        }
