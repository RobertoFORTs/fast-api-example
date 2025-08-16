from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"
    app_name: str = "simple-api"
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = "../.env"

settings = Settings()
