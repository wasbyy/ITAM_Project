from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.handlers import event_router, user_router, admin_router, registration, images_router
from api.login_handler import login_router
from confirm_registration import confirm_router

app = FastAPI(title="ITAM_Project")

# Настройка CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router, tags=["Events"])

app.include_router(user_router, tags=["Users"])

app.include_router(confirm_router, tags=["Confirmations"])

app.include_router(login_router, tags=["Login"], prefix="/login")
app.include_router(admin_router, tags=["Admins"])

app.include_router(registration, tags=["Registration"])

app. include_router(images_router, tags=["Images"])
