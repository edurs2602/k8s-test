from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "FastAPI Backend"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    database_url: str
    database_pool_size: int = 5
    database_max_overflow: int = 10

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def async_database_url(self) -> str:
        url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        url = url.replace("sslmode=require", "ssl=require")
        url = url.replace("&channel_binding=require", "")
        url = url.replace("channel_binding=require&", "")
        url = url.replace("?channel_binding=require", "")
        return url


settings = Settings()