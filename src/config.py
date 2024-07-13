from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    ADMIN_API_KEY: str = "secret key if needed"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "halaio"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    TIMEOUT: int = 60
    SERVER: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
