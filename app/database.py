from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Database data from the docker container
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@db:5432/map"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()