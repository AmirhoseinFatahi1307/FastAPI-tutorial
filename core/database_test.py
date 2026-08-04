from sqlalchemy import create_engine, Column, Integer, String

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


# to create tables and databases
Base.metadata.create_all(engine)
