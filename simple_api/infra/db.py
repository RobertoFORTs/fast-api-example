from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from simple_api.core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    echo=settings.env != "prod",  
    pool_size=10,                 
    max_overflow=20,              
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base(metadata=MetaData(schema="public"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
