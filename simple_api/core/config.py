from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"
    app_name: str = "example-api"

    class Config:
        env_file = ".env"

settings = Settings()
