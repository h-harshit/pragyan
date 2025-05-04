import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # App DB creds
    PG_HOST: str = os.environ["PG_HOST"]
    PG_PORT: str = os.environ["PG_PORT"]
    PG_USER: str = os.environ["PG_USER"]
    PG_PASSWORD: str = os.environ["PG_PASSWORD"]
    PG_APP_DB: str = os.environ["PG_APP_DB"]

    # Redis creds
    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: str = os.environ["REDIS_PORT"]
    REDIS_ACTIVE_CONN_DB_INDEX: str = os.environ["REDIS_ACTIVE_CONN_DB_INDEX"]

    # Security
    FERNET_KEY: str = os.environ["FERNET_KEY"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 1440
    ALGORITHM: str = os.environ["ALGORITHM"]
    USER_TOKEN_URL: str = "/api/v1/auth/user/login"

    # App Config
    DEFAULT_PAGE_SIZE: int = 10


config = Settings()
