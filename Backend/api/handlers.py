from http.client import HTTPResponse
from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select, true, false
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.admin import _create_new_admin
from api.actions.events import _create_new_event, _archive_event, _get_event_by_id, _update_event
from api.actions.user import _create_new_user
from db.models import Event
from db.session import get_db
from api.models import EventCreate, ShowEvent, EventCard, EventUpdateRequest, UpdateEventResponse, UserCreate, ShowUser, \
    ShowAdmin, AdminCreate

event_router = APIRouter()
user_router = APIRouter()

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
    updated_event_id = await _update_event(updated_event_params=updated_event_params, db=db, event_id=event_id)
    return UpdateEventResponse(updated_event_id = updated_event_id)

@user_router.post("/create_user", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_user(body, db)

@admin_router.post("/create_admin", response_model=ShowAdmin)
async def create_admin(body: AdminCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_admin(body, db)