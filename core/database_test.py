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
    lastname = Column(String(length=30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"User (id = {self.id}, firstname = {self.firstname}, lastname = {self.lastname})"


# to create tables and databases
Base.metadata.create_all(engine)


session = Sessionlocal()

# inserting data
# ali = User(firstname="ali", age=31)
# session.add(ali)
# session.commit()

# bulk insert
# mobina = User(firstname="mobina", age=20)
# amir = User(firstname="amir", age=12)
# users = [mobina, amir]
# session.add_all(users)
# session.commit()


# retrieve all data
# users = session.query(User).all()
# print(users)


# retrieve data with filter
users = (
    session.query(User).filter_by(firstname="amir", age=12).one_or_none()
)  # .first()

# updating a record of data
# users.lastname = "fatahi"
# session.commit()

# deleting a data
if users:
    session.delete(users)
    session.commit()
