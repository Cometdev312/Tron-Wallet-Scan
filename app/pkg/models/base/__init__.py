"""Base business models.

All models *must* be inherited by them.
"""

from .exception import BaseAPIException
from .model import BaseModel, Model

__all__ = ("BaseAPIException", "BaseModel", "Model")
