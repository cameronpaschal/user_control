from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.server.controllers.user_controller import router as user_router
from backend.server.controllers.auth_controller import router as auth_router
from backend.infrastructure.db import AsyncDatabase
from backend.infrastructure.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config.load()
    db = AsyncDatabase(config.db)
    await db.init_pool()
    app.state.db = db
    
    try:
        yield
    finally:
        await app.state.db.close_pool()



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",   # your frontend
        "http://localhost:3000",   # if you use React dev server later
        "http://localhost:8081",   # Expo web
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)


    