"""Choosing right pydantic BaseSettings."""

import pydantic

# There is no support for DI in Pydantic V2,
# that's why we inject new BaseSettings into pydantic root
# where DI tries import it.
if int(pydantic.version.VERSION.split(".")[0]) > 1:
    from pydantic_settings import BaseSettings

    pydantic.BaseSettings = BaseSettings
