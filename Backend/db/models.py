from email.policy import strict
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    short_description = Column(String, nullable=True)
    long_description = Column(String, nullable=True)
    max_count_of_members = Column(Integer, nullable=True)
    format = Column(String, nullable=True,default="Online")
    online_event_link = Column(String, nullable=True, default=None)
    tags = Column(String, nullable=True)
    is_active = Column(Boolean, default = True)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role =Column(String, nullable=False)
    age = Column(Integer, nullable=True, default=None)
    course = Column(Integer, nullable=True, default=None)
    university_group = Column(String, nullable=True, default = None)




