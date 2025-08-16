from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, sessionmaker

def get_db(app: FastAPI):
    engine = app.state.engine
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
