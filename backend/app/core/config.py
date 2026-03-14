from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore


class Settings(BaseSettings):
    app_name: str = "AI Quiz Generator Backend"
    app_version: str = "1.0.0"
    debug: bool = True

    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        encoded_password = quote_plus(self.postgres_password)
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{encoded_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )
        
    GROQ_API_KEY: str | None = None


settings = Settings()