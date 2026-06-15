from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# this creates a codeverdict.db file in your project folder
DATABASE_URL = "sqlite:///./codeverdict.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# this function will be used in every route to get a db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()