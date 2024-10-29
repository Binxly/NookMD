import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

TESTING = os.environ.get("TESTING", "0") == "1"

if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False, "timeout": 30},
    )
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./nookmd.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
