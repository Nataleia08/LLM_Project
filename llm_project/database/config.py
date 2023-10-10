from pydantic_settings import BaseSettings
import cloudinary
import os

class Settings(BaseSettings):
    sqlalchemy_database_url: str = ""
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
        
    cloud_name: str = "name"
    cloud_api_key: str = "key"
    cloud_api_secret: str = "sekret"

    openai_api_key: str = "openapikeysekret"

         

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def config_cloudinary():
    return cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.cloud_api_key,
        api_secret=settings.cloud_api_secret,
        secure=True
    )

settings = Settings()


# os.environ["OPENAI_API_KEY"] = settings.open_api_key