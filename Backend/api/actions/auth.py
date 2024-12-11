from typing import Union

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.settings import  SECRET_KEY, ALGORITHM
from db.dals import UserDAL
from db.models import User
from db.session import get_db
from hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def _get_user_by_email_for_auth(email: str, session):
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                email=email,
            )

#существует ли такой юзер
async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        return
    if user.is_active == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "User not confirmed")
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user

async def get_current_user_from_token(
    authorization: str = Security(api_key_header), db: AsyncSession = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split()[-1]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=db)
    if user is None:
        raise credentials_exception
    return user