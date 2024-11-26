from fastapi import FastAPI
from api.handlers import event_router, user_router, admin_router

app = FastAPI(title="ITAM_Project")

app.include_router(event_router, tags=["Events"])

app.include_router(user_router, tags=["Users"])

app.include_router(admin_router, tags=["Admins"])

