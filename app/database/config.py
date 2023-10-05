from pydantic_settings import BaseSettings
import cloudinary

CLOUDINARY = {
    "cloud_name": "dj1qijvd0",
    "api_key": "863185752276523",
    "api_secret": "WUyrtEsJSgjTOHEyev1kMGFamgo"
}

class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql://rtnykatl:xC7vxKxt3yNTUAKmAdHsl7mZhpdKSey1@cornelius.db.elephantsql.com/rtnykatl"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    cloud_name: str = "cloudinary name"
    cloud_api_key: str = "000000000000000000"
    cloud_api_secret: str = "secret"

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