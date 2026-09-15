from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
  APP_NAME: str = "Storage Gateway"

  CLOUD_ENDPOINT: str
  ACCESS_TOKEN: str
  API_KEY: str
  REGION: str = "auto"
  SIGNATURE_VERSION: str
  TTL: int
  BUCKET: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
  )

@lru_cache
def get_settings() -> Settings:
  return Settings()