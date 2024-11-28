from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter, Path
from sqlalchemy import select, true, false
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.admin import _create_new_admin
from api.actions.events import _create_new_event, _archive_event, _get_event_by_id, _update_event
from api.actions.registrations import _check_registrate, _create_new_registration
from api.actions.user import _create_new_user, _get_user_by_id, _update_user
from db.models import Event, User, Registration
from db.session import get_db
from api.models import EventCreate, ShowEvent, EventCard, EventUpdateRequest, UpdateEventResponse, UserCreate, ShowUser, \
    ShowAdmin, AdminCreate, UserCard, UpdateUserResponse, UserUpdateRequest, RegistrationResponse, RegistrationCreate, \
    ShowRegistrationUser, ShowEventInUserCab

event_router = APIRouter()
user_router = APIRouter()

registration = APIRouter()
admin_router = APIRouter()

@event_router.post("/events", response_model=ShowEvent)
async def create_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_event(body, db)

#Показать все активные мероприятия(для главной страницы)
@event_router.get("/events", response_model=List[EventCard])
async def show_all_active_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.is_active == true()))
    events = result.scalars().all()
    return events

#Показать подробную информацию о мероприятии
@event_router.get("/events/{event_id}", response_model=ShowEvent)
async def show_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.event_id == event_id))
    event = result.scalars().first()
    return event

#Архивировать мероприятие
@event_router.patch("/archive_events/{event_id}")
async def archive_event(event_id: int, db: AsyncSession = Depends(get_db)):
    archived_event = await _archive_event(event_id, db)
    if archived_event is None:
        raise HTTPException(status_code=404, detail=f"Event with id: {event_id} not found or already archived")
    return f"{archived_event} event was archived"

@event_router.patch("/events/{event_id}", response_model=UpdateEventResponse)
async def update_event_by_id(event_id: int, body: EventUpdateRequest, db: AsyncSession = Depends(get_db)) -> UpdateEventResponse:
    updated_event_params = body.dict(exclude_none=True)
    if updated_event_params == {}:
        raise HTTPException(status_code=422, detail=f"At least one parameter for event update should be provided")
    event = await _get_event_by_id(event_id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Event with id: {event_id} not found")
    updated_event_id = await _update_event(updated_event_params=updated_event_params, session=db, event_id=event_id)
    return UpdateEventResponse(updated_event_id = updated_event_id)

@user_router.post("/create_user", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)

@user_router.get("/all_users", response_model=List[UserCard])
async def show_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@user_router.patch("/users/{user_id}", response_model=UpdateUserResponse)
async def update_user_by_id(user_id: int, body: UserUpdateRequest, db: AsyncSession = Depends(get_db)):
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail=f"At least one parameter for user update should be provided")
    event = await _get_user_by_id(user_id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    updated_user_id = await _update_user(updated_user_params=updated_user_params, session=db, user_id=user_id)
    return UpdateUserResponse(updated_user_id = updated_user_id)

@admin_router.post("/create_admin", response_model=ShowAdmin)
async def create_admin(body: AdminCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_admin(body, db)

@registration.post("/add_member", response_model=RegistrationResponse)
async def create_registration(body: RegistrationCreate, db: AsyncSession = Depends(get_db)):
    # stmt = select(User).where(User.user_id == body.user_id)
    # result = await db.execute(stmt)
    # user = result.scalar_one_or_none()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # stmt = select(Event).where(Event.event_id == body.event_id)
    # result = await db.execute(stmt)
    # event = result.scalar_one_or_none()
    # if not event:
    #     raise HTTPException(status_code=404, detail="Event not found")
    # check = await _check_registrate(body, db)
    # if check:
    #     raise HTTPException(status_code=400, detail="Already registered for this event")
    return await _create_new_registration(body, db)

@event_router.get("/event_members/{event_id}", response_model=List[ShowRegistrationUser])
async def show_members_on_event(event_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    query = (
        select(User.name, User.surname)
        .join(Registration, Registration.user_id == User.user_id)
        .join(Event, Event.event_id == Registration.event_id)
        .where(Event.event_id == event_id)
    )
    result = await db.execute(query)
    members = result.all()

    members_info = [
        ShowRegistrationUser(name=name, surname=surname) for name, surname in members
    ]

    return members_info


@user_router.get("/user_events/{user_id}", response_model=List[ShowEventInUserCab])
async def show_user_events(user_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    query = (
        select(Event.event_name)
        .join(Registration, Event.event_id == Registration.event_id)
        .join(User, User.user_id == Registration.user_id)
        .where(User.user_id == user_id)
    )
    result = await db.execute(query)
    events = result.all()

    events_info = [
        ShowEventInUserCab(event_name=str(event_name)) for (event_name,) in events
    ]

    return events_info
