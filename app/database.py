from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://zhangeldi:phPeJEIYDKJSxOeHgOPmAeZ9QbA1qXvx@dpg-cvghdv0gph6c73bkg8pg-a.frankfurt-postgres.render.com/saniraq"

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
