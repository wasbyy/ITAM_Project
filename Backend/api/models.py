from typing import Optional

from pydantic import BaseModel, constr
from sqlalchemy import BLOB


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
    description: Optional[constr(min_length=1)]
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


