from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DATABASE: str
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

    class Config:
        env_file = ".env"


class AuthenticationConfig(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


db_config = DatabaseConfig()
auth_config = AuthenticationConfig()
