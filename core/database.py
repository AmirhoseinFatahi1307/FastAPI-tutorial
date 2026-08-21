from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Numeric,
    Date,
    DateTime,
    Time,
    Text,
    Interval,
    Enum,
    ARRAY,
    JSON,
    ForeignKey,
    LargeBinary,
    UUID,
    create_engine,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from enum import Enum as PythonEnum
from sqlalchemy.orm import relationship
from config import settings

# from sqlalchemy ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitemain.db"
# SQLALCHEMY_DATABASE_URL = "sqllite:///:memory:"


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    age = Column(Integer)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
