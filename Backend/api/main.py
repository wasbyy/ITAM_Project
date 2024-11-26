from http.client import HTTPResponse
from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import select, true, false
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.events import _create_new_event, _archive_event, _get_event_by_id, _update_event
from api.handlers import event_router
from db.dals import EventDAL
from db.models import Event
from db.session import get_db
from api.models import EventCreate, ShowEvent, EventCard, EventUpdateRequest, UpdateEventResponse

app = FastAPI(title="ITAM_Project")

main_api_router = APIRouter()

app.include_router(event_router, tags=["Events"])
