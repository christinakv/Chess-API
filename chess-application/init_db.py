from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL

# Create the engine using SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)


def is_db_empty(db_session):
    from sqlalchemy import inspect
    inspector = inspect(db_session.bind)
    return not inspector.get_table_names()


if __name__ == "__main__":
    with SessionLocal() as db:
        if not is_db_empty(db):
            print("Database already exists, skipping initialization.")
        else:
            print("Initializing database...")
            init_db()
            print("Database initialized successfully!")