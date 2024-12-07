import secrets

from api.models import UserCreate, ShowUser
from db.dals import UserDAL
from db.models import User
from hashing import Hasher


async def _create_new_user(body: UserCreate, session):
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                telegram_id=body.telegram_id,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
                telephone_number = body.telephone_number,
                course = body.course,
                university_group = body.university_group,
                confirmation_token = secrets.token_hex(16)
            )
            return user

async def _update_user(updated_user_params: dict, user_id, session):
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(user_id=user_id, **updated_user_params)
            return updated_user_id

async def _get_user_by_id(user_id: int, session) -> ShowUser:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id=user_id)
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    name=user.name,
                    telegram_id=user.telegram_id,
                    role = user.role,
                    email=user.email,
                    telephone_number=user.telephone_number,
                    course=user.course,
                    university_group=user.university_group
                )

def check_user_permissions(target_user: User) -> bool:
    if target_user.role != "admin":
            return False
    return True