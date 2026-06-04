from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Realizar conexão
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@localhost:5433/expressbr_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base para modelos
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
