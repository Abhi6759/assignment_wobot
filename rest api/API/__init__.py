from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, admin

# TO create a new db for the app which stores the user and admin data
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(admin.router)

