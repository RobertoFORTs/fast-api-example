from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: Literal["dev", "prod", "test"] = "dev"
    app_name: str = "simple-api"
    database_url: Optional[str] = None

    class Config:
        env_file = "../.env"

settings = Settings()
