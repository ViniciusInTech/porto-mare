from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str

    tide_api_base_url: str = "https://tabuamare.devtu.qzz.io"
    tide_api_version: str = "v2"
    tide_api_timeout: int = 10
    tide_api_cache_ttl_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
