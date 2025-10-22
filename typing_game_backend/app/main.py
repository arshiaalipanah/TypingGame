from fastapi import FastAPI
from .database import Base, engine
from .routers import users, paragraphs, duel

Base.metadata.create_all(bind=engine)

app = FastAPI(title=" Typing Game Backend ")

app.include_router(users.router)
app.include_router(paragraphs.router)
app.include_router(duel.router)