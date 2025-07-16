# backend/app/create_db.py
from sqlmodel import SQLModel
from models import Comic, User
from database import engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
