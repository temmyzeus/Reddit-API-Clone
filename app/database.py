from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

from .config import db_config

# parse password, So special chars can be used in the database password
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ip_address:port/db"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{db_config.DATABASE_USER}:"
    f"{urllib.parse.quote_plus(db_config.DATABASE_PASSWORD)}"
    f"@{db_config.DATABASE_HOST}"
    f":{db_config.DATABASE_PORT}"
    f"/{db_config.DATABASE}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
