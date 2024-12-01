from email.policy import strict
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)
    place = Column(String, nullable=False)
    short_description = Column(String, nullable=True)
    long_description = Column(String, nullable=True)
    max_count_of_members = Column(Integer, nullable=True)
    format = Column(String, nullable=True,default="Online")
    online_event_link = Column(String, nullable=True, default=None)
    tags = Column(String, nullable=True)
    is_active = Column(Boolean, default = True)
    registrations = relationship('Registration', back_populates='event')

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role =Column(String, nullable=False)
    telephone_number = Column(Integer, nullable=True, default=None)
    course = Column(Integer, nullable=True, default=None)
    university_group = Column(String, nullable=True, default = None)
    registrations = relationship('Registration', back_populates='user')


class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    event_id = Column(Integer, ForeignKey('events.event_id'))
    time_of_registration = Column(DateTime, server_default=func.now())
    user = relationship('User', back_populates='registrations')
    event = relationship('Event', back_populates='registrations')

# class Image(Base):
#     __tablename__ = 'images'
#     id = Column(Integer, primary_key=True)
#     event_id = Column(Integer, ForeignKey('events.event_id'))
#     data = Column(LargeBinary, nullable=False)



