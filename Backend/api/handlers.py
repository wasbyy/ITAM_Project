from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Path, Form
from sqlalchemy import select, true, func, delete, false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.notifications import send_email, send_reminder
from db.dals import EventDAL

from api.actions.admin import _create_new_admin
from api.actions.auth import get_current_user_from_token
from api.actions.events import _archive_event, _update_event
from api.actions.registrations import _create_new_registration
from api.actions.user import _create_new_user, _get_user_by_id, _update_user, check_user_permissions
from confirm_registration import send_confirmation_email
from db.models import Event, User, Registration, Image
from db.session import get_db
from api.models import ShowEvent, EventCard, EventUpdateRequest, UpdateEventResponse, UserCreate, \
    ShowAdmin, AdminCreate, UserCard, UpdateUserResponse, UserUpdateRequest, ShowRegistrationUser, ShowEventInUserCab, \
    UserInfoInCab
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import File, UploadFile, HTTPException, Depends
from PIL import Image as PillowImage

event_router = APIRouter()
user_router = APIRouter()
registration = APIRouter()
admin_router = APIRouter()
images_router = APIRouter()

archiving_router = APIRouter()

scheduler = AsyncIOScheduler()

@event_router.post("/events")
async def create_event_with_image(
    event_name: str = Form(...),
    place: str = Form(...),
    short_description: str = Form(...),
    long_description: str = Form(...),
    max_count_of_members: int = Form(...),
    online_event_link: str = Form(...),
    format: str = Form(...),
    date: datetime = Form(...),
    tags: str = Form(...),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)):

    if not check_user_permissions(current_user):
        raise HTTPException(status_code=403, detail="Forbidden.")

    async with db.begin():
        event_dal = EventDAL(db)
        event = await event_dal.create_event(
        event_name=event_name,
        place=place,
        short_description = short_description,
        long_description=long_description,
        max_count_of_members=max_count_of_members,
        format=format,
        date=date,
        online_event_link=online_event_link,
        tags=tags
        )

    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file is not an image")

        file_data = await file.read()

        try:
            img = PillowImage.open(BytesIO(file_data))

            width, height = img.size

            if width != height:
                raise HTTPException(status_code=400, detail="The image must be square.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")

        new_image = Image(event_id=event.event_id, data=file_data)
        db.add(new_image)
        await db.commit()
        await db.refresh(new_image)

    schedule_event_reminder(event.event_id, event.date)
    return {
        "message": "Event created successfully.",
        "event_id": event.event_id,
        "image_uploaded": bool(file),
    }

@event_router.get("/events", response_model=List[EventCard])
async def show_all_active_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.is_active == true()))
    events = result.scalars().all()
    return events

@event_router.get("/events/{event_id}", response_model=ShowEvent)
async def show_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.event_id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")
    return event

@event_router.patch("/archive_events/{event_id}")
async def archive_event(event_id: int, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    archived_event = await _archive_event(event_id, db)
    if archived_event is None:
        raise HTTPException(status_code=404, detail=f"Event with id: {event_id} not found or already archived")
    return f"{archived_event} event was archived"

@event_router.patch("/events/{event_id}", response_model=UpdateEventResponse,)
async def update_event_by_id(event_id: int, body: EventUpdateRequest, db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user_from_token)) -> UpdateEventResponse:
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    updated_event_params = body.dict(exclude_none=True)
    if updated_event_params == {}:
        raise HTTPException(status_code=422, detail=f"At least one parameter for event update should be provided")
    updated_event_id = await _update_event(updated_event_params=updated_event_params, session=db, event_id=event_id)
    result = await db.execute(
        select(Registration)
        .join(User, Registration.user_id == User.user_id)
        .where(Registration.event_id == event_id)
        .options(joinedload(Registration.user))
    )
    registrations = result.scalars().all()

    emails = [reg.user.email for reg in registrations]

    event_result = await db.execute(select(Event).where(Event.event_id == event_id))
    event = event_result.scalar_one_or_none()

    subject = f"Изменения в мероприятии: {event.event_name}"
    body = (
        "Дорогой участник мероприятий ITAM,\n\n"
        f"Мероприятие {event.event_name} было изменено.\n\n"
        "Просим обратить внимание на изменения, будем ждать вас на мероприятии!\n\n"
        "С наилучшими пожеланиями,\n"
        "Команда ITAM"
    )

    for email in emails:
        await send_email(email, subject, body)
    return UpdateEventResponse(updated_event_id = updated_event_id)

@event_router.get("/event_members/{event_id}", response_model=List[ShowRegistrationUser])
async def show_members_on_event(event_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user_from_token)):
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    query = (
        select(User.name, Registration.time_of_registration)
        .join(Registration, Registration.user_id == User.user_id)
        .join(Event, Event.event_id == Registration.event_id)
        .where(Event.event_id == event_id)
    )
    result = await db.execute(query)
    members = result.all()

    members_info = [
        ShowRegistrationUser(name=name, time_of_registration=time_of_registration) for name, time_of_registration in members
    ]

    return members_info

@event_router.get("/count_members/{event_id}")
async def count_events(event_id: int, db: AsyncSession = Depends(get_db)):
    query = select(func.count()).select_from(Registration).where(Registration.event_id == event_id)
    result = await db.execute(query)
    counter = result.scalar_one()
    return counter

@event_router.delete("/delete_event/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    result = await db.execute(
        select(Registration)
        .join(User, Registration.user_id == User.user_id)
        .where(Registration.event_id == event_id)
        .options(joinedload(Registration.user))
    )
    registrations = result.scalars().all()

    emails = [reg.user.email for reg in registrations]

    event_result = await db.execute(select(Event).where(Event.event_id == event_id))
    event = event_result.scalar_one_or_none()

    subject = f"Изменения в мероприятии: {event.event_name}"
    body = (
        "Дорогой участник мероприятий ITAM,\n\n"
        f"К сожалению, мероприятие {event.event_name} было отменено.\n\n"
        "Приносим извинения за предоставленные неудобства, ждем вас на других мероприятиях!\n\n"
        "С наилучшими пожеланиями,\n"
        "Команда ITAM"
    )

    # Отправляем уведомления каждому участнику
    for email in emails:
        await send_email(email, subject, body)

    stmt_image = delete(Image).where(
        Image.event_id == event_id,
    )
    await db.execute(stmt_image)

    stmt_registration = delete(Registration).where(
        Registration.event_id == event_id,
    )
    await db.execute(stmt_registration)

    stmt_event = delete(Event).where(
        Event.event_id == event_id,
    )
    result_event = await db.execute(stmt_event)

    await db.commit()

    if result_event.rowcount == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"You deleted {event_id} event"}

@event_router.get("/archived_events", response_model=List[EventCard])
async def show_all_archived_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.is_active == false()))
    events = result.scalars().all()
    return events

@user_router.post("/create_user")
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await _create_new_user(body, db)
    await send_confirmation_email(new_user.email, new_user.confirmation_token)
    return {"message": "Registration successful, please confirm your email"}

#Вспомогательная ручка
@user_router.get("/all_users", response_model=List[UserCard])
async def show_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.get("/users_info", response_model=UserInfoInCab)
async def show_user_info(db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    result = await db.execute(select(User).where(User.user_id == current_user.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    return user


@user_router.patch("/users", response_model=UpdateUserResponse)
async def update_user_by_id(body: UserUpdateRequest, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.user_id
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail=f"At least one parameter for user update should be provided")
    event = await _get_user_by_id(user_id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    updated_user_id = await _update_user(updated_user_params=updated_user_params, session=db, user_id=user_id)
    return UpdateUserResponse(updated_user_id = updated_user_id)

@user_router.get("/user_events", response_model=List[ShowEventInUserCab])
async def show_user_events(db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.user_id
    query = (
        select(Event.event_id, Event.event_name, Event.date)
        .join(Registration, Event.event_id == Registration.event_id)
        .join(User, User.user_id == Registration.user_id)
        .where(User.user_id == user_id)
    )
    result = await db.execute(query)
    events = result.all()

    events_info = [ShowEventInUserCab(event_id = event_id, event_name=event_name, date=date) for event_id, event_name, date in events]

    return events_info

@user_router.get("/user_completed_events", response_model=List[ShowEventInUserCab])
async def show_user_completed_events(db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.user_id
    query = (
        select(Event.event_id,Event.event_name, Event.date)
        .join(Registration, Event.event_id == Registration.event_id)
        .join(User, User.user_id == Registration.user_id)
        .where(User.user_id == user_id, Event.is_active == False)
    )
    result = await db.execute(query)
    events = result.all()

    events_info = [ShowEventInUserCab(event_id = event_id, event_name=event_name, date=date) for event_id, event_name, date in events]

    return events_info

@user_router.get("/user_role")
async def user_role(current_user: User = Depends(get_current_user_from_token)):
    user_role = current_user.role
    return user_role

@user_router.get("/check_user_registration")
async def check_registrate(event_id: int,  db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user_from_token)):
    stmt = select(Registration).where(Registration.event_id == event_id, Registration.user_id == current_user.user_id)
    result = await db.execute(stmt)
    reg = result.scalar_one_or_none()
    await db.commit()
    if reg:
        return True
    return False


@admin_router.post("/create_admin", response_model=ShowAdmin)
async def create_admin(body: AdminCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_admin(body, db)


@registration.post("/add_member")
async def create_registration(event_id: int, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user_from_token)):
    stmt = select(Event).where(Event.event_id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    stmt1 = select(Registration).where(Registration.event_id == event_id, Registration.user_id == current_user.user_id)
    result1 = await db.execute(stmt1)
    reg = result1.scalar_one_or_none()
    await db.commit()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if await count_events(event_id, db) >= event.max_count_of_members:
        raise HTTPException(status_code=403, detail="Maximum number of members reached.")
    await db.commit()
    if reg:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    email_subject = f"Уведомление о регистрации на мероприятие {event.event_name}"
    email_body = (
        f"Уважаемый участник мероприятий ITAM,\n\n"
        f"Вы были успешно зарегистрированы на мероприятие: {event.event_name}.\n\n"
        f"Подробности данного мероприятия:\n"
        f"- Описание: {event.long_description}\n"
        f"- Дата проведения: {event.date}\n"
        f"- Место проведения: {event.place}\n\n"
        f"Будем рады видеть вас!\n\n"
        f"С наилучшими пожеланиями,\n"
        f"Команда ITAM"
    )
    await send_email(current_user.email, email_subject, email_body)
    return await _create_new_registration(current_user.user_id, event_id, db)


@registration.delete("/cancel_registration")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    stmt = delete(Registration).where(
        Registration.event_id == event_id,
        Registration.user_id == current_user.user_id,
    )
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Registration not found")

    return {"message": f"You canceled registration"}


@images_router.get("/show_event_image/{event_id}")
async def download_image(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Image).where(Image.event_id == event_id))
    image = result.scalars().first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image_stream = BytesIO(image.data)
    return StreamingResponse(image_stream, media_type="image/jpeg")

def schedule_event_reminder(event_id: int, event_date: datetime):
    """
    Планирует задачу отправки напоминания за 24 часа до начала мероприятия.
    """
    reminder_time = event_date - timedelta(hours=24)
    if reminder_time > datetime.now():
        scheduler.add_job(
            send_reminder,
            "date",
            run_date=reminder_time,
            args=[event_id],
            id=f"event_{event_id}_reminder",
        )
        print(f"Reminder scheduled for event {event_id} at {reminder_time}.")
    else:
        print(f"Event {event_id} is too close to schedule a reminder.")

# Запуск планировщика при старте приложения
@user_router.on_event("startup")
async def start_scheduler():
    scheduler.start()