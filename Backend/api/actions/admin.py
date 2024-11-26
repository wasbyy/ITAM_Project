from api.models import AdminCreate, ShowAdmin
from db.dals import UserDAL, AdminDAL
from hashing import Hasher


async def _create_new_admin(body: AdminCreate, session) -> ShowAdmin:
        async with session.begin():
            admin_dal = AdminDAL(session)
            admin = await admin_dal.create_admin(
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
            )
            return ShowAdmin(
            user_id = admin.user_id,
            name = admin.name,
            surname = admin.surname,
            email = admin.email,
            )

# async def _update_admin(updated_user_params: dict, user_id, session):
#         async with session.begin():
#             admin_dal = UserDAL(session)
#             updated_user_id = await user_dal.update_user(user_id=user_id, **updated_user_params)
#             return updated_user_id
#
# async def _get_user_by_id(user_id: int, session) -> ShowUser:
#         async with session.begin():
#             user_dal = UserDAL(session)
#             user = await user_dal.get_user_by_id(user_id=user_id)
#             if user is not None:
#                 return ShowUser(
#                     user_id=user.user_id,
#                     name=user.name,
#                     surname=user.surname,
#                     email=user.email,
#                     age=user.age,
#                     course=user.course,
#                     university_group=user.university_group
#                 )