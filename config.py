from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str

    class Config:
        env_file = ".env"

settings = Settings()
