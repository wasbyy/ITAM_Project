from datetime import datetime
from typing import Union
from uuid import UUID
import secrets

from fastapi import UploadFile, File
from sqlalchemy import and_, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.images import upload_image
from db.models import Event, User, Registration

class EventDAL:
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_event(self, event_name: str, place: str, short_description: str, long_description: str, max_count_of_members: int,
                           online_event_link:str, format: str, date: datetime, tags: str) -> Event:
        new_event = Event(
            event_name=event_name,
            place=place,
            short_description=short_description,
            long_description=long_description,
            max_count_of_members=max_count_of_members,
            online_event_link=online_event_link,
            date = date,
            format = format,
            tags=tags,
)
        self.db_session.add(new_event)
        await self.db_session.flush()
        return new_event

    async def archive_event(self, event_id: int) -> Union[Event, None]:
        query = update(Event).where(and_(Event.event_id == event_id, Event.is_active == True)).values(
            is_active=False).returning(Event.event_id)
        res = await self.db_session.execute(query)
        # res.fetchone(): Извлекает первую строку результата запроса.
        archive_event_id_row = res.fetchone()
        if archive_event_id_row is not None:
            return archive_event_id_row[0]

    async def update_event(self, event_id: int, **kwargs) -> Union[Event, None]:
        query = update(Event).where(Event.event_id == event_id).values(kwargs).returning(
            Event.event_id)
        res = await self.db_session.execute(query)
        updated_event_id_row = res.fetchone()
        if updated_event_id_row is not None:
            return updated_event_id_row[0]

    async def get_event_by_id(self, event_id: int) -> Union[Event, None]:
        query = select(Event).where(Event.event_id == event_id)
        res = await self.db_session.execute(query)
        event_row = res.fetchone()
        if event_row is not None:
            return event_row[0]


class UserDAL:
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, name: str, email: str, hashed_password: str, telephone_number: str, telegram_id: str,
        course: int, university_group: str, confirmation_token: str, is_active: bool =  False) -> User:
        new_user = User(
            name=name, telegram_id = telegram_id, email=email, hashed_password=hashed_password, role="user",
            telephone_number=telephone_number, course=course, university_group=university_group,
            confirmation_token = confirmation_token, is_active=is_active
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(self, user_id: int, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

class AdminDAL():
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_admin(
            self, name: str, email: str, hashed_password: str, telephone_number: str = None,
            course: int = None, university_group: str = None, telegram_id: str = None, confirmation_token: str = None) -> User:
        new_user = User(
            name=name, email=email, telegram_id = telegram_id, hashed_password=hashed_password, role="admin",
            telephone_number=telephone_number,course=course, university_group = university_group,
            confirmation_token= confirmation_token, is_active=True
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

class RegistrationDAL():
    def __init__(self, db_session=AsyncSession):
        self.db_session = db_session

    async def create_registration(
            self, user_id, event_id,
    ):
        new_registrations = Registration(
            user_id=user_id, event_id=event_id
        )
        self.db_session.add(new_registrations)
        await self.db_session.flush()
        return new_registrations

    async def get_user_in_registration_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        users_row = res.fetchone()
        if users_row is not None:
            return users_row[0]