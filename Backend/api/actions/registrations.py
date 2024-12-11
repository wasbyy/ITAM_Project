from fastapi import Depends
from sqlalchemy import select

from db.dals import RegistrationDAL
from db.models import Registration
from db.session import get_db


# Проверка наличия существующей регистрации
async def _check_registrate(event_id: int, db=Depends(get_db)):
    stmt = select(Registration).where(
        Registration.event_id == event_id
    )
    result = await db.execute(stmt)
    existing_registration = result.scalar_one_or_none()
    return existing_registration

# Создание новой регистрации
async def _create_new_registration(user_id, event_id, session):
    async with session.begin():
        registration_dal = RegistrationDAL(session)
        registration = await registration_dal.create_registration(
            user_id=user_id,
            event_id=event_id,
        )
        if registration:
            return {"resp": "Successfully registered"}
