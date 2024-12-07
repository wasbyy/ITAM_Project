from typing import List

from fastapi import Depends, HTTPException, APIRouter, Path, File, UploadFile
from sqlalchemy import select, true, func, delete
from sqlalchemy.ext.asyncio import AsyncSession


from api.actions.admin import _create_new_admin
# from api.actions.archiving import start_scheduler
from api.actions.auth import get_current_user_from_token
from api.actions.events import _create_new_event, _archive_event, _get_event_by_id, _update_event
from api.actions.registrations import _create_new_registration
from api.actions.user import _create_new_user, _get_user_by_id, _update_user, check_user_permissions
from confirm_registration import send_confirmation_email
from db.models import Event, User, Registration, Image
from db.session import get_db
from api.models import EventCreate, ShowEvent, EventCard, EventUpdateRequest, UpdateEventResponse, UserCreate, ShowUser, \
    ShowAdmin, AdminCreate, UserCard, UpdateUserResponse, UserUpdateRequest, ShowRegistrationUser, ShowEventInUserCab
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

@event_router.post("/events")
async def create_event(body: EventCreate, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    return await _create_new_event(body, db)

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
    event = await _get_event_by_id(event_id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Event with id: {event_id} not found")
    updated_event_id = await _update_event(updated_event_params=updated_event_params, session=db, event_id=event_id)
    return UpdateEventResponse(updated_event_id = updated_event_id)

@event_router.get("/event_members/{event_id}", response_model=List[ShowRegistrationUser])
async def show_members_on_event(event_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(get_current_user_from_token)):
    if not check_user_permissions(
        current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    query = (
        select(User.name, User.surname, Registration.time_of_registration)
        .join(Registration, Registration.user_id == User.user_id)
        .join(Event, Event.event_id == Registration.event_id)
        .where(Event.event_id == event_id)
    )
    result = await db.execute(query)
    members = result.all()

    members_info = [
        ShowRegistrationUser(name=name, surname=surname, time_of_registration=time_of_registration) for name, surname, time_of_registration in members
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
    stmt = delete(Event).where(
        Event.event_id == event_id,
    )
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": f"You deleted {event_id} event"}

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


@user_router.patch("/users/{user_id}", response_model=UpdateUserResponse)
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

@user_router.get("/user_events/{user_id}", response_model=List[ShowEventInUserCab])
async def show_user_events(db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.user_id
    query = (
        select(Event.event_name)
        .join(Registration, Event.event_id == Registration.event_id)
        .join(User, User.user_id == Registration.user_id)
        .where(User.user_id == user_id)
    )
    result = await db.execute(query)
    events = result.all()

    events_info = [
        ShowEventInUserCab(event_name=str(event_name, date)) for (event_name, date) in events
    ]
    return events_info

@admin_router.post("/create_admin", response_model=ShowAdmin)
async def create_admin(body: AdminCreate, db: AsyncSession = Depends(get_db)):
    return await _create_new_admin(body, db)

@registration.post("/add_member")
async def create_registration(event_id: int, db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user_from_token)):
        # stmt = select(Event).where(Event.event_id == body.event_id)
        # result = await db.execute(stmt)
        # event = result.scalar_one_or_none()
        # if not event:
        #     raise HTTPException(status_code=404, detail="Event not found")
        # check = await _check_registrate(body, db)
        # if check:
        #     raise HTTPException(status_code=400, detail="Already registered for this event")
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

@images_router.post("/upload_event_image/{event_id}")
async def upload_image(
        event_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    # Проверка типа файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Чтение содержимого файла
    file_data = await file.read()

    try:
        # Открываем файл как изображение с помощью библиотеки Pillow
        img = PillowImage.open(BytesIO(file_data))

        # Получаем размеры изображения
        width, height = img.size

        # Проверяем, является ли изображение квадратным
        if width != height:
            raise HTTPException(status_code=400, detail="The image must be square.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")

    # Если проверка прошла успешно, сохраняем изображение в базу данных
    new_image = Image(event_id=event_id, data=file_data)  # Ваш класс Image остается без изменений
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {"message": f"Image for event {event_id} uploaded successfully"}

@images_router.get("/show_event_image/{event_id}")
async def download_image(event_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем изображение из базы данных
    result = await db.execute(select(Image).where(Image.event_id == event_id))
    image = result.scalars().first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Преобразуем бинарные данные в поток
    image_stream = BytesIO(image.data)
    return StreamingResponse(image_stream, media_type="image/jpeg")

# @archiving_router.on_event('startup')
# async def startup(db: AsyncSession = Depends(get_db)):
#     await db.connect()
#     await start_scheduler()
#
#
# # Закрываем соединение с базой данных при остановке сервера
# @archiving_router.on_event('shutdown')
# async def shutdown(db: AsyncSession = Depends(get_db)):
#     await db.disconnect()
