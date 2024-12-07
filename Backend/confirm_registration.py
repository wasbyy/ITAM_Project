import aiosmtplib
from email.mime.text import MIMEText

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_db
from db.settings import my_email, password

async def send_confirmation_email(email: str, token: str):
    confirmation_url = f"http://localhost:8000/confirm/{token}"
    message = MIMEText(f"Click the link to confirm your registration: {confirmation_url}")
    message["Subject"] = "Email Confirmation"
    message["From"] = my_email
    message["To"] = email

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username= my_email,
            password= password
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send confirmation email")


confirm_router = APIRouter()


@confirm_router.get("/confirm/{token}")
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.confirmation_token == token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    query = (update(User).where(User.confirmation_token == token).values(is_active=True, confirmation_token = None)
             .returning(User.user_id))
    res = await db.execute(query)
    await db.commit()
    edit_user = res.fetchone()
    if edit_user is not None:
        return {"message": "Email confirmed successfully"}