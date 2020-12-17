import databases
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

database = databases.Database(DATABASE_URL)

metadata: MetaData = sqlalchemy.MetaData()

Base = declarative_base()
