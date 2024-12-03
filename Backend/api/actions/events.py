from fastapi import UploadFile, File

from api.actions.images import upload_image, download_image
from api.models import EventCreate, ShowEvent
from db.dals import EventDAL


async def _create_new_event(body: EventCreate, session):
    async with session.begin():
        event_dal = EventDAL(session)
        await event_dal.create_event(
        event_name=body.event_name,
        # image = file,
        place=body.place,
        short_description = body.short_description,
        long_description=body.long_description,
        max_count_of_members=body.max_count_of_members,
        format=body.format,
        online_event_link=body.online_event_link,
        tags=body.tags
        )
        return {"message": f"Event created"}


async def _archive_event(event_id, session):
    async with session.begin():
        event_dal = EventDAL(session)
        archived_event = await event_dal.archive_event(event_id=event_id)
        return archived_event

async def _update_event(updated_event_params: dict, event_id, session):
    async with session.begin():
        event_dal = EventDAL(session)
        updated_user_id = await event_dal.update_event(event_id=event_id, **updated_event_params)
        return updated_user_id

async def _get_event_by_id(event_id: int, session) -> ShowEvent:
    async with session.begin():
        event_dal = EventDAL(session)
        event = await event_dal.get_event_by_id(event_id=event_id)
        if event is not None:
            return ShowEvent(
                event_id=event.event_id,
                event_name=event.event_name,
                place=event.place,
                long_description=event.long_description,
                max_count_of_members=event.max_count_of_members,
                online_event_link=event.online_event_link,
                format = event.format,
                tags=event.tags,
                is_active=event.is_active
            )


