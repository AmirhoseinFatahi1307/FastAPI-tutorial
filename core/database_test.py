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


# all users
users_all = session.query(User).all()

# query all users with age greater than or equal to 25
users_filtered = session.query(User).filter(User.age >= 25).all()

print("ALL Users: ", len(users_all))
print("Filtered Users: ", len(users_filtered))
# add multiple filters
# query all users with age greater than or equal to 25 and name equals to something
users_filtered = (
    session.query(User).filter(User.age >= 25, User.firstname == "ali").all()
)

# or you can use where
users_filtered = (
    session.query(User).where(User.age >= 25, User.firstname == "ali").all()
)

# users with similar name contianing specific substrings
users_similar_name = session.query(User).filter(User.firstname.like("%ali%")).all()

# users with case insensitive match
users_similar_name = session.query(User).filter(User.firstname.ilike("%ali%")).all()

# users with starting and ending chars
users_starting_ali = session.query(User).filter(User.firstname.like("Ali%")).all()
users_ending_ali = session.query(User).filter(User.firstname.like("%Ali")).all()


from sqlalchemy import or_, and_, not_

# query those who has ali as name or age above 25
users_filtered = (
    session.query(User).filter(or_(User.age >= 25, User.firstname == "ali")).all()
)

# query those who has ali as name and age above 25
users_filtered = (
    session.query(User).filter(and_(User.age >= 25, User.firstname == "ali")).all()
)

# query those whos name is not ali
users_filtered = session.query(User).filter(not_(User.firstname == "ali")).all()

# getting users which are note named ali or age between 35,60
users = session.query(User).filter(
    or_(not_(User.firstname == "ali"), and_(User.age > 35, User.age < 60))
)


from sqlalchemy.sql import func

# 1. Count Total Users
total_users = session.query(func.count(User.id)).scalar()
print("Total Users:", total_users)

# 2. Find the Average Age of Users
average_age = session.query(func.avg(User.age)).scalar()
print("Average Age:", average_age)

# 3. Find the Maximum and Minimum Age
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Max Age: {max_age}, Min Age: {min_age}")

# 4. Find the Total Number of Orders
# total_orders = session.query(func.count(Order.id)).scalar()
# print("Total Orders:", total_orders)

# 5. Find the Sum of All Order Amounts
# total_revenue = session.query(func.sum(Order.total_amount)).scalar()
# print("Total Revenue:", total_revenue)

# 6. Find the Average Order Value
# average_order_value = session.query(func.avg(Order.total_amount)).scalar()
# print("Average Order Value:", average_order_value)

# 7. Find Users Who Have Placed the Most Orders
# most_active_users = (
#     session.query(User.name, func.count(Order.id).label("order_count"))
#     .join(Order)
#     .group_by(User.id)
#     .order_by(func.count(Order.id).desc())
#     .limit(5)
#     .all()
# )
# print("Top 5 Active Users by Order Count:", most_active_users)

# 8. Find Users with the Highest Total Spending
# top_spenders = (
#     session.query(User.name, func.sum(Order.total_amount).label("total_spent"))
#     .join(Order)
#     .group_by(User.id)
#     .order_by(func.sum(Order.total_amount).desc())
#     .limit(5)
#      .all()
# )
# print("Top 5 Users by Spending:", top_spenders)

# 9. Find Users Who Have Not Placed Any Orders
# users_without_orders = (
#    session.query(User).outerjoin(Order).filter(Order.id == None).all()
# )
# print("Users Without Orders:", [user.name for user in users_without_orders])

# 10. Find the Most Recent Order Date
# latest_order_date = session.query(func.max(Order.created_at)).scalar()
# print("Most Recent Order Date:", latest_order_date)

# Close the session
# session.close()
