# app/settings/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app.settings.config import Settings

settings = Settings() # pyright: ignore

SQLALCHEMY_DATABASE_URL = (
	f"mysql+mysqldb://"
	f"{settings.db_user}"
	f":{settings.db_pass}"
	f"@{settings.db_host}"
	f":{settings.db_port}"
	f"/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
	"""Create a ORM local session with the database and closes when finished."""
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()