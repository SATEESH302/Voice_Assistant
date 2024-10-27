from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from constants import DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'interview_assist'}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)