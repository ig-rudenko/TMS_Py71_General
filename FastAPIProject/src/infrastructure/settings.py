from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite+aiosqlite:///sqlite3.db"

    redis_host: str = ""
    redis_password: str | None = None
    redis_port: int = 6379
    redis_db: int = 0
    redis_max_connections: int = 5


settings = Settings()
