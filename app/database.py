from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

from .config import database_config


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ip_address/db"
SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{database_config.DATABASE_USER}:{urllib.parse.quote_plus(database_config.DATABASE_PASSWORD)}@{database_config.DATABASE_HOST}:{database_config.DATABASE_PORT}/{database_config.DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
