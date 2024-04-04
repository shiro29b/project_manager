from fastapi import Body, Depends, FastAPI
from .routers import users,auth,projects
from . import models

from .database import engine


models.Base.metadata.create_all(bind=engine)

app =FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)


@app.get("/")
def root():
    return {"message": "Hello World?"}