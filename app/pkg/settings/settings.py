"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""

from functools import lru_cache
from typing import Optional
import pydantic
from dotenv import find_dotenv
from pydantic.types import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("get_settings", )


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.

    Examples:
        `.env` file should look like::

            TELEGRAM__TOKEN=...
            TELEGRAM__WEBHOOK_DOMAIN_URL=...

            LOGGER__PATH_TO_LOG="./src/logs"
            LOGGER__LEVEL="DEBUG"

            API_SERVER__HOST="127.0.0.1"
            API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g., my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also:
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        arbitrary_types_allowed=True,
        case_sensitive=True,
        env_nested_delimiter="__",
        extra="allow",
    )


class Database(_Settings):
    """Database settings."""

    #: str: Database host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of database.
    PORT: PositiveInt = 5432
    #: str: Database user.
    USER: str = "postgres"
    #: SecretStr: Database password.
    PASSWORD: SecretStr = SecretStr("postgres")
    #: str: Database database name.
    DATABASE_NAME: str = "postgres"

    def get_dsn(self, is_async: bool = False) -> str:
        driver = "postgresql"
        if is_async:
            driver = "postgresql+asyncpg"

        return f'{driver}://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}'


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """

    #: SecretStr: secret x-token for authority.
    X_API_TOKEN: pydantic.SecretStr

    #: Bool: Debug mode flag
    DEBUG: Optional[bool] = True

    #: Database: Database settings.
    DATABASE: Database


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
