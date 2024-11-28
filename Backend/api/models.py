from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, constr


#Конвертирует все что не словарь в json
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
    online_event_link: str
    tags: str

class ShowEvent(TunedModel):
    event_name: str
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
    event_name: str
    short_description: str
    place: str
    tags: str

class UpdateEventResponse(BaseModel):
    updated_event_id: int

class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    age: int
    course: int
    university_group: str

class ShowUser(BaseModel):
    user_id: int
    name: str
    surname: str
    email: str
    age: int
    course: int
    university_group: str

class AdminCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class ShowAdmin(BaseModel):
    user_id: int
    name: str
    surname: str
    email: str

class UserCard(TunedModel):
    user_id: int
    name: str
    surname: str
    email: str
    role: str
    age: Optional[int] = None
    course: Optional[int] = None
    university_group: Optional[str] = None

class UserUpdateRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[constr(min_length=1)]
    age: Optional[int]
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
    surname: str

class ShowEventInUserCab(TunedModel):
    event_name: str
