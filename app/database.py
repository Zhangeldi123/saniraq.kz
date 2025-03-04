from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://nfactorial:d9H17TdfSn4fPePLtvcZAYoeKxMcuOF0@dpg-cv3knihu0jms73ait6qg-a.frankfurt-postgres.render.com/shaniraq"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
