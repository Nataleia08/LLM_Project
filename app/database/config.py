from pydantic_settings import BaseSettings
import cloudinary


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql://rtnykatl:xC7vxKxt3yNTUAKmAdHsl7mZhpdKSey1@cornelius.db.elephantsql.com/rtnykatl"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    cloud_name: str = "ddizyikxv"
    cloud_api_key: str = "936543749716439"
    cloud_api_secret: str = "Dza4eAZ2qkSbkQC4Kmfpj1Lf1SE"
          

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