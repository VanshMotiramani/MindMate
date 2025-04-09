from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_port: str
    database_name: str
    database_username: str
    token_expire_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()