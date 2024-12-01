from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, constr


#Конвертирует все что не словарь в json
class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True

class EventCreate(BaseModel):
    event_name: str
    # image: bytes
    place: str
    short_description: str
    long_description: str
    max_count_of_members: int
    format: str
    online_event_link: str
    tags: str

class ShowEvent(TunedModel):
    event_name: str
    # image: bytes
    place: str
    long_description: str
    max_count_of_members: int
    online_event_link: str
    format: str
    tags: str
    is_active: bool

class EventUpdateRequest(BaseModel):
    event_name: Optional[constr(min_length=1)]
    place: Optional[constr(min_length=1)]
    long_description: Optional[constr(min_length=1)]
    short_description: Optional[constr(min_length=1)]
    max_count_of_members: Optional[int]
    online_event_link: Optional[constr(min_length=1)]
    tags: Optional[constr(min_length=1)]

class EventCard(TunedModel):
    event_id: int
    # image: bytes
    event_name: str
    short_description: str
    place: str
    tags: str

class UpdateEventResponse(BaseModel):
    updated_event_id: int

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    telephone_number: int
    course: int
    university_group: str

class ShowUser(BaseModel):
    user_id: int
    name: str
    email: str
    telephone_number: int
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
    email: str
    role: str
    telephone_number: Optional[int] = None
    course: Optional[int] = None
    university_group: Optional[str] = None

class UserUpdateRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    email: Optional[constr(min_length=1)]
    telephone_number: Optional[int]
    course: Optional[int]
    university_group: Optional[constr(min_length=1)]

class UpdateUserResponse(BaseModel):
    updated_user_id: int

class RegistrationCreate(BaseModel):
    user_id: int
    event_id: int

class RegistrationResponse(BaseModel):
    resp: str

class ShowRegistrationUser(TunedModel):
    name: str
    time_of_registration: datetime

class ShowEventInUserCab(TunedModel):
    event_name: str

