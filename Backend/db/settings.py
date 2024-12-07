from envparse import Env

env = Env()

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/itam_project"

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.environ.get("my_gmail")
password = os.environ.get("password_gmail")
