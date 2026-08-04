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
)
from enum import Enum as PythonEnum
from sqlalchemy.orm import relationship

# from sqlalchemy ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqllite:///:memory:"


# for postgres or other relartional databases
# SQLALCHEMY_DATABASE_URL = "postgres://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(length=30))
    lastname = Column(String(length=30))
    age = Column(Integer)

    def __repr__(self):
        return f"User (id = {self.id}, firstname = {self.firstname}, lastname = {self.lastname})"


class UserType(PythonEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class SampleModel(Base):
    __tablename__ = "sample_model"

    id = Column(Integer, primary_key=True)
    string_field = Column(String(100))
    text_field = Column(Text)
    boolean_field = Column(Boolean)
    integer_field = Column(Integer)
    float_field = Column(Float)
    numeric_field = Column(Numeric(10, 2))
    date_field = Column(Date)
    datetime_field = Column(DateTime)
    time_field = Column(Time)
    interval_field = Column(Interval)
    enum_field = Column(Enum(UserType))
    array_field = Column(ARRAY(Integer))
    json_field = Column(JSON)
    uuid_field = Column(UUID)
    foreign_key_field = Column(Integer, ForeignKey("related_table.id"))
    binary_field = Column(LargeBinary)


# to create tables and databases
Base.metadata.create_all(engine)
