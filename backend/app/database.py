from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

# Makes a new database session for each request
SessionLocal = sessionmaker(bind=engine)


# Gives a route a session, then closes it when the request finishes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
