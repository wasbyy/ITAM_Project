import aiosmtplib
from email.message import EmailMessage

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event, Registration, User
from db.session import get_db
from db.settings import my_email, password
from sqlalchemy.future import select

SMTP_CONFIG = {
    "hostname": "smtp.gmail.com",
    "port": 465,
    "username": my_email,
    "password": password,
}

async def send_email(recipient_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = SMTP_CONFIG["username"]
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=SMTP_CONFIG["hostname"],
        port=SMTP_CONFIG["port"],
        username=SMTP_CONFIG["username"],
        password=SMTP_CONFIG["password"],
        use_tls=True,
    )


async def send_reminder(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.event_id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        print(f"Event with ID {event_id} not found.")
        return

    # Извлекаем участников мероприятия
    registrations_result = await db.execute(
        select(Registration)
        .join(User, Registration.user_id == User.user_id)
        .where(Registration.event_id == event_id)
    )
    registrations = registrations_result.scalars().all()
    emails = [reg.user.email for reg in registrations]

    # Содержание письма
    subject = f"Reminder: {event.event_name}"
    body = (
        "Уважаемый участник мероприятий ITAM,\n\n"
        f"Напоминаем что через 24 часа будет проводится мероприятие: {event.event_name}.\n\n"
        f"Подробнее о мероприятии:\n"
        f"- Описание: {event.long_description}\n"
        f"- Дата проведения: {event.date}\n"
        f"- Место проведения: {event.place}\n\n"
        f"Будем рады видеть вас!\n\n"
        "Команда ITAM"
    )

    for email in emails:
        await send_email(email, subject, body)