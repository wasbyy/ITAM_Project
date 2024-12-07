from api.models import AdminCreate, ShowAdmin
from db.dals import AdminDAL
from hashing import Hasher


async def _create_new_admin(body: AdminCreate, session) -> ShowAdmin:
        async with session.begin():
            admin_dal = AdminDAL(session)
            admin = await admin_dal.create_admin(
                name=body.name,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
            )
            return ShowAdmin(
            user_id = admin.user_id,
            name = admin.name,
            email = admin.email,
            )