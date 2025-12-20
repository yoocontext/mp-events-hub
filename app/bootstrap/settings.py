from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PgSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    db: str = Field(default="events-hub", alias="PG__DB")
    user: str = Field(default="admin", alias="PG__USER")
    password: str = Field(default="admin", alias="PG__PASSWORD")
    host: str = Field(default="events-hub", alias="PG__HOST")
    port: str = Field(default="5432", alias="PG__PORT")

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RmqSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    username: str = Field(alias="RMQ__USERNAME", default="RMQ_USERNAME")
    password: str = Field(alias="RMQ__PASSWORD", default="RMQ_PASSWORD")
    host: str = Field(alias="RMQ__HOST", default="localhost")
    port: int = Field(alias="RMQ__PORT", default=5672)

    @property
    def rabbit_broker_url(self) -> str:
        return rf"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    host: str = Field(alias="REDIS__HOST", default="localhost")
    port: int = Field(alias="REDIS__PORT", default=6379)
    db: int = Field(alias="REDIS__DB", default=0)
    password: str = Field(alias="REDIS__PASSWORD", default="")


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    secret_key: str = Field(default="", alias="AUTH__SECRET_KEY")
    access_token_lifetime: int = Field(
        default=5_000_000_000,
        alias="AUTH__ACCESS_TOKEN_LIFETIME",
    )
    algorithm: str = Field(default="sha256", alias="AUTH__ALGORITHM")
    confirm_code_ttl_sec_int: int = Field(
        default=600,
        alias="AUTH__CONFIRM_CODE_TTL_SEC",
    )
    reset_password_ttl_sec_int: int = Field(
        default=600,
        alias="AUTH__RESET_PASSWORD_TTL_SEC",
    )

    @property
    def confirm_code_ttl_sec(self) -> timedelta:
        return timedelta(seconds=self.confirm_code_ttl_sec_int)

    @property
    def reset_password_ttl(self) -> timedelta:
        return timedelta(seconds=self.reset_password_ttl_sec_int)

class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    smtp_host: str = Field(default="localhost", alias="EMAIL__SMTP_HOST")
    smtp_port: int = Field(default=25, alias="EMAIL__SMTP_PORT")
    username: str = Field(default="user", alias="EMAIL__USERNAME")
    password: str = Field(default="", alias="EMAIL__PASSWORD")


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    login: str = Field(default="login", alias="MINIO__LOGIN")
    password: str = Field(default="password", alias="MINIO__PASSWORD")
    aws_access_key_id: str = Field(default="id", alias="MINIO__AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="key", alias="MINIO__AWS_SECRET_ACCESS_KEY")
    endpoint_url: str = Field(default="endpoint", alias="MINIO__ENDPOINT_URL")


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    host: str = Field(alias="ELASTIC__HOST", default="ELC_HOST")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    pg: PgSettings = PgSettings()
    rmq: RmqSettings = RmqSettings()
    redis: RedisSettings = RedisSettings()
    minio: MinioSettings = MinioSettings()
    elastic: ElasticSettings = ElasticSettings()
    auth: AuthSettings = AuthSettings()
    email: EmailSettings = EmailSettings()


def get_settings() -> Settings:
    return Settings()