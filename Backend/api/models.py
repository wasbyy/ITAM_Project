from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True

class EventCreate(BaseModel):
    event_name: str
    place: str
    short_description: str
    long_description: str
    max_count_of_members: int
    format: str
    date: datetime
    online_event_link: str
    tags: str

class ShowEvent(TunedModel):
    event_name: str
    place: str
    long_description: str
    short_description: str
    max_count_of_members: int
    online_event_link: str
    format: str
    date: datetime
    tags: str
    is_active: bool

class EventUpdateRequest(BaseModel):
    event_name: Optional[str]
    place: Optional[str]
    long_description: Optional[str]
    short_description: Optional[str]
    max_count_of_members: Optional[int]
    online_event_link: Optional[str]
    format: Optional[str]
    date: Optional[datetime]
    tags: Optional[str]

class EventCard(TunedModel):
    event_id: int
    event_name: str
    short_description: str
    date: datetime
    place: str
    tags: str

class UpdateEventResponse(BaseModel):
    updated_event_id: int

class UserInfoInCab(TunedModel):
    user_id: int
    telegram_id: Optional[str] = None
    name: str
    email: str
    telephone_number: Optional[str] = None
    course: Optional[int] = None
    university_group: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    telegram_id: str
    email: str
    password: str
    telephone_number: str
    course: int
    university_group: str

class ShowUser(BaseModel):
    user_id: int
    telegram_id: str
    name: str
    email: str
    telephone_number: str
    course: int
    university_group: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str

class ShowAdmin(BaseModel):
    user_id: int
    name: str
    email: str

class UserCard(TunedModel):
    user_id: int
    name: str
    telegram_id: str
    email: str
    role: str
    telephone_number: Optional[str] = None
    course: Optional[int] = None
    university_group: Optional[str] = None

class UserUpdateRequest(BaseModel):
    name: Optional[str]
    email: Optional[str]
    telegram_id: Optional[str]
    telephone_number: Optional[str]
    course: Optional[int]
    university_group: Optional[str]

class UpdateUserResponse(BaseModel):
    updated_user_id: int

class RegistrationResponse(BaseModel):
    resp: str

class ShowRegistrationUser(TunedModel):
    name: str
    time_of_registration: datetime

class ShowEventInUserCab(TunedModel):
    event_id: int
    event_name: str
    date: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

