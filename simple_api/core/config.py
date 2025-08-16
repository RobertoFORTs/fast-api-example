from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"
    app_name: str = "simple-api"
    database_url: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
