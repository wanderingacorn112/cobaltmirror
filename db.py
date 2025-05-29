# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN", "postgresql+psycopg://osint:super-secret@localhost:5432/osint")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)