# global configs

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "Face Service"
    oauth_token_secret: str = "face_service_secret"
    log_level: str = "DEBUG"


settings = Settings()  # type: ignore